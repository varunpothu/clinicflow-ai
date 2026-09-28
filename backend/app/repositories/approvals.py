from datetime import UTC, datetime
from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.approval import Approval
from app.models.proposal import Proposal


class ApprovalRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, proposal: Proposal) -> Approval:
        approval = Approval(
            id=uuid4(),
            proposal_id=UUID(proposal.id),
            proposal_version=proposal.version,
            status="PENDING",
            expires_at=proposal.expires_at,
        )
        self.session.add(approval)
        await self.session.flush()
        return approval

    async def get_for_proposal(self, proposal_id: UUID) -> Approval | None:
        result = await self.session.execute(
            select(Approval)
            .where(Approval.proposal_id == proposal_id)
            .order_by(Approval.id)
        )
        return result.scalars().first()

    async def decide(
        self,
        *,
        approval_id: UUID,
        expected_version: int,
        approver_id: UUID,
        decision: str,
        reason: str | None = None,
        now: datetime | None = None,
    ) -> Approval:
        result = await self.session.execute(
            select(Approval).where(Approval.id == approval_id)
        )
        approval = result.scalar_one()
        current_time = now or datetime.now(UTC)
        if approval.status != "PENDING":
            raise ValueError("APPROVAL_NOT_PENDING")
        if approval.proposal_version != expected_version:
            raise ValueError("STALE_PROPOSAL")
        if current_time >= approval.expires_at:
            approval.status = "EXPIRED"
            raise ValueError("APPROVAL_EXPIRED")
        if decision not in {"APPROVED", "REJECTED"}:
            raise ValueError("INVALID_DECISION")

        approval.status = decision
        approval.approver_id = approver_id
        approval.decision_reason = reason
        approval.decided_at = current_time
        await self.session.flush()
        return approval
