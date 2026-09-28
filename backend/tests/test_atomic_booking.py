from datetime import UTC, datetime, timedelta
from uuid import UUID, uuid4

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.db.base import Base
from app.models.approval import Approval
from app.models.audit_event import AuditEvent
from app.models.outbox import OutboxEvent
from app.repositories.approvals import ApprovalRepository
from app.repositories.booking import AtomicBookingService
from app.repositories.proposals import ProposalRepository


@pytest.mark.asyncio
async def test_atomic_booking_creates_appointment_audit_and_outbox() -> None:
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    session_factory = async_sessionmaker(engine, expire_on_commit=False)
    proposal_id = uuid4()
    patient_id = uuid4()
    clinician_id = uuid4()
    actor_id = uuid4()
    start = datetime.now(UTC) + timedelta(days=1)

    async with session_factory() as session:
        proposals = ProposalRepository(session)
        approvals = ApprovalRepository(session)
        proposal = await proposals.create(
            proposal_id=proposal_id,
            request_id=uuid4(),
            patient_id=patient_id,
            clinician_id=clinician_id,
            appointment_type="routine",
            starts_at=start,
            ends_at=start + timedelta(minutes=30),
            expires_at=start + timedelta(minutes=15),
            rationale="integration-test",
        )
        approval = await approvals.create(proposal)
        await session.commit()

        service = AtomicBookingService(session)
        result = await service.approve_and_book(
            proposal_id=proposal_id,
            approval_id=UUID(str(approval.id)),
            proposal_version=1,
            actor_id=actor_id,
            idempotency_key="integration-approval-001",
            correlation_id="corr-integration-001",
        )

        assert result["proposal_id"] == proposal_id.hex

        appointments = await session.execute(select(Approval))
        assert appointments.scalar_one().status == "APPROVED"

        audit = await session.execute(select(AuditEvent))
        assert audit.scalar_one().event_type == "APPOINTMENT_CONFIRMED"

        outbox = await session.execute(select(OutboxEvent))
        assert outbox.scalar_one().event_type == "APPOINTMENT_CONFIRMED"

    await engine.dispose()
