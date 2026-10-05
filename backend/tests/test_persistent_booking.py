from datetime import UTC, datetime, timedelta
from uuid import uuid4

import pytest
import pytest_asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.db.base import Base
from app.models import Appointment, Approval, AuditEventRecord, OutboxEvent, Proposal
from app.services.persistent_approval import PersistentApprovalService


@pytest_asyncio.fixture
async def session_factory() -> async_sessionmaker:
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    return async_sessionmaker(engine, expire_on_commit=False)


def build_proposal(proposal_id, patient_id, clinician_id, now):
    return Proposal(
        id=str(proposal_id),
        request_id=str(uuid4()),
        patient_id=str(patient_id),
        clinician_id=str(clinician_id),
        appointment_type="routine",
        starts_at=now + timedelta(hours=1),
        ends_at=now + timedelta(hours=1, minutes=30),
        version=1,
        status="PENDING",
        expires_at=now + timedelta(minutes=10),
        rationale="test",
    )


@pytest.mark.asyncio
async def test_persistent_approval_creates_booking_audit_and_outbox(session_factory) -> None:
    proposal_id = uuid4()
    patient_id = uuid4()
    clinician_id = uuid4()
    now = datetime.now(UTC)

    async with session_factory() as session:
        session.add(build_proposal(proposal_id, patient_id, clinician_id, now))
        session.add(
            Approval(
                id=uuid4(),
                proposal_id=proposal_id,
                proposal_version=1,
                status="PENDING",
                expires_at=now + timedelta(minutes=10),
            )
        )
        await session.commit()

    async with session_factory() as session:
        result = await PersistentApprovalService(session).approve(
            proposal_id=proposal_id,
            proposal_version=1,
            approver_id=uuid4(),
            idempotency_key="persistent-approve-001",
            correlation_id="corr-001",
            now=now,
        )
        assert result["status"] == "CONFIRMED"

        appointments = (await session.execute(select(Appointment))).scalars().all()
        audits = (await session.execute(select(AuditEventRecord))).scalars().all()
        outbox = (await session.execute(select(OutboxEvent))).scalars().all()

        assert len(appointments) == 1
        assert len(audits) == 1
        assert len(outbox) == 1


@pytest.mark.asyncio
async def test_second_approval_with_same_key_returns_same_result(session_factory) -> None:
    proposal_id = uuid4()
    now = datetime.now(UTC)

    async with session_factory() as session:
        session.add(build_proposal(proposal_id, uuid4(), uuid4(), now))
        await session.commit()

    actor = uuid4()
    key = "persistent-approve-002"
    async with session_factory() as session:
        first = await PersistentApprovalService(session).approve(
            proposal_id=proposal_id,
            proposal_version=1,
            approver_id=actor,
            idempotency_key=key,
            correlation_id="corr-002",
            now=now,
        )
    async with session_factory() as session:
        second = await PersistentApprovalService(session).approve(
            proposal_id=proposal_id,
            proposal_version=1,
            approver_id=actor,
            idempotency_key=key,
            correlation_id="corr-002",
            now=now,
        )
    assert first == second


@pytest.mark.asyncio
async def test_stale_proposal_is_rejected(session_factory) -> None:
    proposal_id = uuid4()
    now = datetime.now(UTC)

    async with session_factory() as session:
        session.add(build_proposal(proposal_id, uuid4(), uuid4(), now))
        await session.commit()

    async with session_factory() as session:
        with pytest.raises(ValueError, match="STALE_PROPOSAL"):
            await PersistentApprovalService(session).approve(
                proposal_id=proposal_id,
                proposal_version=2,
                approver_id=uuid4(),
                idempotency_key="persistent-approve-003",
                correlation_id="corr-003",
                now=now,
            )
