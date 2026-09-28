from datetime import datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.proposal import Proposal


class ProposalRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(
        self,
        *,
        proposal_id: UUID,
        request_id: UUID,
        patient_id: UUID,
        clinician_id: UUID,
        appointment_type: str,
        starts_at: datetime,
        ends_at: datetime,
        expires_at: datetime,
        rationale: str,
        version: int = 1,
    ) -> Proposal:
        proposal = Proposal(
            id=str(proposal_id),
            request_id=str(request_id),
            patient_id=str(patient_id),
            clinician_id=str(clinician_id),
            appointment_type=appointment_type,
            starts_at=starts_at,
            ends_at=ends_at,
            expires_at=expires_at,
            rationale=rationale,
            version=version,
            status="PENDING",
        )
        self.session.add(proposal)
        await self.session.flush()
        return proposal

    async def get(self, proposal_id: UUID) -> Proposal | None:
        result = await self.session.execute(
            select(Proposal).where(Proposal.id == str(proposal_id))
        )
        return result.scalar_one_or_none()
