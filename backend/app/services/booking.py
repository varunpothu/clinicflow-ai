from datetime import UTC, datetime
from typing import TypedDict
from uuid import UUID, uuid4

from app.domain.idempotency import IdempotencyStore
from app.domain.proposal import AppointmentProposal
from app.services.demo_store import DemoStore


class BookingConflict(Exception):
    pass


class BookingResult(TypedDict):
    appointment: dict[str, object]
    approved_by: str
    proposal_id: str
    proposal_version: int


class BookingService:
    def __init__(
        self,
        store: DemoStore | None = None,
        idempotency: IdempotencyStore[BookingResult] | None = None,
    ) -> None:
        self.store = store or DemoStore()
        self.idempotency = idempotency or IdempotencyStore[BookingResult]()

    def approve_and_book(
        self,
        *,
        idempotency_key: str,
        patient_id: UUID,
        proposal: AppointmentProposal,
        actor_id: UUID,
        now: datetime | None = None,
    ) -> BookingResult:
        current_time = now or datetime.now(UTC)
        fingerprint = (
            f"{proposal.proposal_id}:{proposal.version}:{proposal.clinician_id}:"
            f"{proposal.starts_at.isoformat()}:{patient_id}"
        )
        existing = self.idempotency.get(idempotency_key)
        if existing:
            if existing.fingerprint != fingerprint:
                raise ValueError("IDEMPOTENCY_KEY_REUSE")
            return existing.result

        if current_time >= proposal.expires_at:
            raise ValueError("PROPOSAL_EXPIRED")

        if not self.store.slot_is_available(proposal.clinician_id, proposal.starts_at):
            raise BookingConflict("BOOKING_CONFLICT")

        appointment = self.store.book(
            appointment_id=str(uuid4()),
            clinician_id=proposal.clinician_id,
            starts_at=proposal.starts_at,
            ends_at=proposal.ends_at,
            patient_id=patient_id,
            appointment_type=proposal.appointment_type,
        )
        result: BookingResult = {
            "appointment": appointment,
            "approved_by": str(actor_id),
            "proposal_id": str(proposal.proposal_id),
            "proposal_version": proposal.version,
        }
        self.idempotency.put(idempotency_key, fingerprint, result)
        return result
