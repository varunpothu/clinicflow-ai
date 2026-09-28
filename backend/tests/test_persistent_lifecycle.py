from datetime import UTC, datetime, timedelta
from uuid import uuid4

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.db.base import Base
from app.models import Appointment, AuditEventRecord, OutboxEvent
from app.services.persistent_lifecycle import PersistentAppointmentLifecycleService


async def build_session():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    return async_sessionmaker(engine, expire_on_commit=False)


@pytest.mark.asyncio
async def test_cancel_persists_audit_and_outbox() -> None:
    factory = await build_session()
    appointment_id = uuid4()
    now = datetime.now(UTC)
    async with factory() as session:
        session.add(Appointment(
            id=appointment_id,
            patient_id=uuid4(),
            clinician_id=uuid4(),
            appointment_type="routine",
            starts_at=now + timedelta(hours=1),
            ends_at=now + timedelta(hours=1, minutes=30),
            status="CONFIRMED",
            version=1,
        ))
        await session.commit()

    async with factory() as session:
        result = await PersistentAppointmentLifecycleService(session).cancel(
            appointment_id=appointment_id,
            actor_id=uuid4(),
            idempotency_key="cancel-0001",
            correlation_id="corr-cancel-1",
        )
        assert result["status"] == "CANCELLED"
        assert len((await session.execute(select(AuditEventRecord))).scalars().all()) == 1
        assert len((await session.execute(select(OutboxEvent))).scalars().all()) == 1


@pytest.mark.asyncio
async def test_reschedule_rejects_stale_version() -> None:
    factory = await build_session()
    appointment_id = uuid4()
    now = datetime.now(UTC)
    async with factory() as session:
        session.add(Appointment(
            id=appointment_id,
            patient_id=uuid4(),
            clinician_id=uuid4(),
            appointment_type="routine",
            starts_at=now + timedelta(hours=1),
            ends_at=now + timedelta(hours=1, minutes=30),
            status="CONFIRMED",
            version=2,
        ))
        await session.commit()

    async with factory() as session:
        with pytest.raises(ValueError, match="STALE_APPOINTMENT"):
            await PersistentAppointmentLifecycleService(session).reschedule(
                appointment_id=appointment_id,
                actor_id=uuid4(),
                new_starts_at=now + timedelta(hours=2),
                new_ends_at=now + timedelta(hours=2, minutes=30),
                expected_version=1,
                idempotency_key="reschedule-0001",
                correlation_id="corr-reschedule-1",
            )
