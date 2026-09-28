from datetime import UTC, datetime
from uuid import uuid4

import pytest
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.db.base import Base
from app.repositories.workflows import WorkflowEventRepository


@pytest.mark.asyncio
async def test_workflow_event_sequence_is_monotonic() -> None:
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    session_factory = async_sessionmaker(engine, expire_on_commit=False)
    workflow_id = uuid4()

    async with session_factory() as session:
        repo = WorkflowEventRepository(session)
        first = await repo.append(
            workflow_id=workflow_id,
            event_type="REQUEST_RECEIVED",
            state="RECEIVED",
            occurred_at=datetime.now(UTC),
        )
        second = await repo.append(
            workflow_id=workflow_id,
            event_type="EXTRACTION_STARTED",
            state="EXTRACTING",
            occurred_at=datetime.now(UTC),
        )
        await session.commit()

        events = await repo.list_for_workflow(workflow_id)
        assert first.sequence_number == 1
        assert second.sequence_number == 2
        assert [event.event_type for event in events] == [
            "REQUEST_RECEIVED",
            "EXTRACTION_STARTED",
        ]

    await engine.dispose()
