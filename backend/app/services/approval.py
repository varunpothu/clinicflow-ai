from uuid import UUID

from app.services.booking import BookingConflict, BookingResult, BookingService
from app.services.proposal_store import ProposalStore


class ApprovalService:
    def __init__(
        self,
        proposals: ProposalStore | None = None,
        booking: BookingService | None = None,
    ) -> None:
        self.proposals = proposals or ProposalStore()
        self.booking = booking or BookingService()

    def approve(
        self,
        *,
        proposal_id: UUID,
        proposal_version: int,
        actor_id: UUID,
        idempotency_key: str,
    ) -> BookingResult:
        record = self.proposals.get(proposal_id)
        if record is None:
            raise ValueError("PROPOSAL_NOT_FOUND")
        if record.proposal.version != proposal_version:
            raise ValueError("STALE_PROPOSAL")
        try:
            return self.booking.approve_and_book(
                idempotency_key=idempotency_key,
                patient_id=record.patient_id,
                proposal=record.proposal,
                actor_id=actor_id,
            )
        except BookingConflict:
            raise
