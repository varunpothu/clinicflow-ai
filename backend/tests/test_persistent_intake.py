from uuid import uuid4

import pytest
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.core.config import Settings
from app.db.base import Base
from app.models.appointment_request import AppointmentRequest
from app.services.persistent_intake import PersistentIntakeService


@pytest.mark.asyncio
async def test_request_is_persisted_and_idempotent() -> None:
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    factory = async_sessionmaker(engine, expire_on_commit=False)

    patient = uuid4()
    async with factory() as session:
        service = PersistentIntakeService(session, Settings(ai_provider="mock"))
        first = await service.create(
            patient_id=patient,
            appointment_type="routine",
            natural_language="Tuesday after 4pm",
            idempotency_key="request-0001",
        )

    async with factory() as session:
        record = await session.get(AppointmentRequest, first["request_id"])
        assert record is not None
        assert record.status == "VALIDATING"

    async with factory() as session:
        second = await PersistentIntakeService(session, Settings(ai_provider="mock")).create(
            patient_id=patient,
            appointment_type="routine",
            natural_language="Tuesday after 4pm",
            idempotency_key="request-0001",
        )

    assert first == second
