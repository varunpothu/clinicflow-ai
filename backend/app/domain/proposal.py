from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4


@dataclass(frozen=True)
class AppointmentProposal:
    proposal_id: UUID
    request_id: UUID
    clinician_id: UUID
    appointment_type: str
    starts_at: datetime
    ends_at: datetime
    version: int
    expires_at: datetime
    rationale: str

    @classmethod
    def create(
        cls,
        *,
        request_id: UUID,
        clinician_id: UUID,
        appointment_type: str,
        starts_at: datetime,
        ends_at: datetime,
        version: int,
        expires_at: datetime,
        rationale: str,
    ) -> "AppointmentProposal":
        return cls(
            proposal_id=uuid4(),
            request_id=request_id,
            clinician_id=clinician_id,
            appointment_type=appointment_type,
            starts_at=starts_at,
            ends_at=ends_at,
            version=version,
            expires_at=expires_at,
            rationale=rationale,
        )
