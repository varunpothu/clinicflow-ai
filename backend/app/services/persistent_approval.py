from datetime import UTC, datetime
import json
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.appointments import AppointmentRepository
from app.repositories.approvals import ApprovalRepository
from app.repositories.audit import AuditRepository
from app.repositories.idempotency import PersistentIdempotencyRepository
from app.repositories.outbox import OutboxRepository
from app.repositories.proposals import ProposalRepository


class PersistentApprovalService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.proposals = ProposalRepository(session)
        self.approvals = ApprovalRepository(session)
        self.appointments = AppointmentRepository(session)
        self.idempotency = PersistentIdempotencyRepository(session)
        self.audit = AuditRepository(session)
        self.outbox = OutboxRepository(session)

    async def approve(
        self,
        *,
        proposal_id: UUID,
        proposal_version: int,
        approver_id: UUID,
        idempotency_key: str,
        correlation_id: str,
        now: datetime | None = None,
    ) -> dict[str, object]:
        current_time = now or datetime.now(UTC)
        fingerprint = f"{proposal_id}:{proposal_version}:{approver_id}"

        async with self.session.begin():
            existing = await self.idempotency.get(idempotency_key)
            if existing is not None:
                if existing.fingerprint != fingerprint:
                    raise ValueError("IDEMPOTENCY_KEY_REUSE")
                decoded = json.loads(existing.result_json)
                if not isinstance(decoded, dict):
                    raise ValueError("IDEMPOTENCY_RECORD_INVALID")
                return decoded

            proposal = await self.proposals.get(proposal_id)
            if proposal is None:
                raise ValueError("PROPOSAL_NOT_FOUND")

            if proposal.version != proposal_version:
                raise ValueError("STALE_PROPOSAL")

            if proposal.status != "PENDING":
                raise ValueError("PROPOSAL_NOT_PENDING")

            if current_time >= proposal.expires_at:
                proposal.status = "EXPIRED"
                raise ValueError("PROPOSAL_EXPIRED")

            approval = await self.approvals.get_for_proposal(proposal_id)
            if approval is not None:
                if approval.proposal_version != proposal_version:
                    raise ValueError("STALE_PROPOSAL")
                if approval.status != "PENDING":
                    raise ValueError("APPROVAL_NOT_PENDING")
                approval.status = "APPROVED"
                approval.approver_id = approver_id
                approval.decided_at = current_time

            try:
                async with self.session.begin_nested():
                    appointment = await self.appointments.create(
                        patient_id=UUID(proposal.patient_id),
                        clinician_id=UUID(proposal.clinician_id),
                        appointment_type=proposal.appointment_type,
                        starts_at=proposal.starts_at,
                        ends_at=proposal.ends_at,
                    )
            except IntegrityError as exc:
                raise ValueError("APPOINTMENT_CONFLICT") from exc

            proposal.status = "APPROVED"
            result: dict[str, object] = {
                "appointment_id": str(appointment.id),
                "proposal_id": str(proposal.id),
                "proposal_version": proposal.version,
                "status": "CONFIRMED",
            }

            await self.audit.record(
                event_type="APPOINTMENT_CONFIRMED",
                summary="Appointment confirmed after authorised human approval.",
                correlation_id=correlation_id,
                actor_id=approver_id,
                entity_id=appointment.id,
                metadata={"proposal_version": str(proposal.version)},
                occurred_at=current_time,
            )
            await self.outbox.add(
                aggregate_id=appointment.id,
                event_type="APPOINTMENT_CONFIRMED",
                payload=result | {"correlation_id": correlation_id},
                occurred_at=current_time,
            )
            await self.idempotency.put(
                idempotency_key,
                fingerprint,
                result,
            )
            return result
