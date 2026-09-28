from datetime import UTC, datetime, timedelta
from uuid import uuid4

import pytest
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.db.base import Base
from app.repositories.appointments import AppointmentConflictError, AppointmentRepository


@pytest.mark.asyncio
async def test_active_appointment_conflict_is_database_protected() -> None:
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    session_factory = async_sessionmaker(engine, expire_on_commit=False)
    clinician_id = uuid4()
    start = datetime.now(UTC) + timedelta(days=1)
    end = start + timedelta(minutes=30)

    async with session_factory() as session:
        repository = AppointmentRepository(session)
        await repository.create(
            patient_id=uuid4(),
            clinician_id=clinician_id,
            appointment_type="routine",
            starts_at=start,
            ends_at=end,
        )
        await session.commit()

    async with session_factory() as session:
        repository = AppointmentRepository(session)
        with pytest.raises(AppointmentConflictError, match="APPOINTMENT_CONFLICT"):
            await repository.create(
                patient_id=uuid4(),
                clinician_id=clinician_id,
                appointment_type="routine",
                starts_at=start,
                ends_at=end,
            )

    await engine.dispose()


@pytest.mark.asyncio
async def test_cancelled_slot_can_be_reused() -> None:
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    session_factory = async_sessionmaker(engine, expire_on_commit=False)
    clinician_id = uuid4()
    start = datetime.now(UTC) + timedelta(days=1)
    end = start + timedelta(minutes=30)

    async with session_factory() as session:
        repository = AppointmentRepository(session)
        appointment = await repository.create(
            patient_id=uuid4(),
            clinician_id=clinician_id,
            appointment_type="routine",
            starts_at=start,
            ends_at=end,
        )
        appointment.status = "CANCELLED"
        await session.commit()

        await repository.create(
            patient_id=uuid4(),
            clinician_id=clinician_id,
            appointment_type="routine",
            starts_at=start,
            ends_at=end,
        )
        await session.commit()

    await engine.dispose()
