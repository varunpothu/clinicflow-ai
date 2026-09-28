import json
from datetime import UTC, datetime
from typing import cast
from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.proposal import Proposal
from app.repositories.approvals import ApprovalRepository
from app.repositories.appointments import AppointmentConflictError, AppointmentRepository
from app.repositories.audit import AuditRepository
from app.repositories.idempotency import PersistentIdempotencyRepository
from app.repositories.outbox import OutboxRepository
from app.repositories.proposals import ProposalRepository


class AtomicBookingService:
    """Persistent approval-to-book transaction with audit and outbox side effects."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.proposals = ProposalRepository(session)
        self.approvals = ApprovalRepository(session)
        self.appointments = AppointmentRepository(session)
        self.audit = AuditRepository(session)
        self.outbox = OutboxRepository(session)
        self.idempotency = PersistentIdempotencyRepository(session)

    async def approve_and_book(
        self,
        *,
        proposal_id: UUID,
        approval_id: UUID,
        proposal_version: int,
        actor_id: UUID,
        idempotency_key: str,
        correlation_id: str,
        now: datetime | None = None,
    ) -> dict[str, object]:
        current_time = now or datetime.now(UTC)

        async with self.session.begin():
            proposal = await self.proposals.get(proposal_id)
            if proposal is None:
                raise ValueError("PROPOSAL_NOT_FOUND")
            if proposal.version != proposal_version:
                raise ValueError("STALE_PROPOSAL")
            if current_time >= proposal.expires_at:
                raise ValueError("PROPOSAL_EXPIRED")

            existing = await self.idempotency.get(idempotency_key)
            if existing is not None:
                if existing.fingerprint != self._fingerprint(proposal):
                    raise ValueError("IDEMPOTENCY_KEY_REUSE")
                cached = json.loads(existing.result_json)
                if not isinstance(cached, dict):
                    raise ValueError("IDEMPOTENCY_RECORD_INVALID")
                return cast(dict[str, object], cached)

            try:
                appointment = await self.appointments.create(
                    patient_id=UUID(proposal.patient_id),
                    clinician_id=UUID(proposal.clinician_id),
                    appointment_type=proposal.appointment_type,
                    starts_at=proposal.starts_at,
                    ends_at=proposal.ends_at,
                )
            except (AppointmentConflictError, IntegrityError):
                raise ValueError("APPOINTMENT_CONFLICT") from None

            approval_result = await self.approvals.decide(
                approval_id=approval_id,
                expected_version=proposal_version,
                approver_id=actor_id,
                decision="APPROVED",
                now=current_time,
            )

            await self.audit.record(
                event_type="APPOINTMENT_CONFIRMED",
                summary="Appointment booked after authorised approval",
                correlation_id=correlation_id,
                actor_id=actor_id,
                entity_id=appointment.id,
                metadata={
                    "proposal_id": proposal_id.hex,
                    "approval_id": str(approval_result.id),
                },
                occurred_at=current_time,
            )
            await self.outbox.add(
                aggregate_id=appointment.id,
                event_type="APPOINTMENT_CONFIRMED",
                payload={
                    "appointment_id": str(appointment.id),
                    "proposal_id": proposal_id.hex,
                    "correlation_id": correlation_id,
                },
                occurred_at=current_time,
            )
            result = {
                "appointment_id": str(appointment.id),
                "proposal_id": proposal_id.hex,
                "proposal_version": proposal_version,
                "approved_by": str(actor_id),
            }
            await self.idempotency.put(
                idempotency_key,
                self._fingerprint(proposal),
                result,
            )
            return result

    @staticmethod
    def _fingerprint(proposal: Proposal) -> str:
        return f"{proposal.id}:{proposal.version}:{proposal.clinician_id}:{proposal.starts_at}"
