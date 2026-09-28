from datetime import UTC, datetime, timedelta
from uuid import uuid4

import pytest
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.db.base import Base
from app.repositories.approvals import ApprovalRepository
from app.repositories.proposals import ProposalRepository


@pytest.mark.asyncio
async def test_approval_requires_matching_proposal_version() -> None:
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    session_factory = async_sessionmaker(engine, expire_on_commit=False)
    async with session_factory() as session:
        proposal_repo = ProposalRepository(session)
        approval_repo = ApprovalRepository(session)
        proposal = await proposal_repo.create(
            proposal_id=uuid4(),
            request_id=uuid4(),
            patient_id=uuid4(),
            clinician_id=uuid4(),
            appointment_type="routine",
            starts_at=datetime.now(UTC) + timedelta(days=1),
            ends_at=datetime.now(UTC) + timedelta(days=1, minutes=30),
            expires_at=datetime.now(UTC) + timedelta(minutes=10),
            rationale="test",
        )
        approval = await approval_repo.create(proposal)
        with pytest.raises(ValueError, match="STALE_PROPOSAL"):
            await approval_repo.decide(
                approval_id=approval.id,
                expected_version=2,
                approver_id=uuid4(),
                decision="APPROVED",
            )

    await engine.dispose()
