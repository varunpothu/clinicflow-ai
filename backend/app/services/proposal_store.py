from datetime import UTC, datetime
from uuid import UUID

from app.domain.proposal import AppointmentProposal


class ProposalRecord:
    def __init__(self, proposal: AppointmentProposal, patient_id: UUID) -> None:
        self.proposal = proposal
        self.patient_id = patient_id
        self.created_at = datetime.now(UTC)


class ProposalStore:
    def __init__(self) -> None:
        self._records: dict[UUID, ProposalRecord] = {}

    def save(self, proposal: AppointmentProposal, patient_id: UUID) -> ProposalRecord:
        record = ProposalRecord(proposal, patient_id)
        self._records[proposal.proposal_id] = record
        return record

    def get(self, proposal_id: UUID) -> ProposalRecord | None:
        return self._records.get(proposal_id)
