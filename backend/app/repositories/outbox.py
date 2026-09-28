import json
from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.outbox import OutboxEvent


class OutboxRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(
        self,
        *,
        aggregate_id: UUID,
        event_type: str,
        payload: dict[str, object],
        occurred_at: datetime,
    ) -> OutboxEvent:
        event = OutboxEvent(
            id=uuid4(),
            aggregate_id=aggregate_id,
            event_type=event_type,
            payload=json.dumps(payload, sort_keys=True, default=str),
            occurred_at=occurred_at,
            attempt_count=0,
        )
        self.session.add(event)
        await self.session.flush()
        return event
