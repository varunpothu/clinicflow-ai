import json
from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.integrations.sqs import EventPublisher
from app.models.outbox import OutboxEvent


class OutboxDispatcher:
    def __init__(self, session: AsyncSession, publisher: EventPublisher) -> None:
        self.session = session
        self.publisher = publisher

    async def dispatch_batch(self, limit: int = 50) -> int:
        result = await self.session.execute(
            select(OutboxEvent)
            .where(OutboxEvent.published_at.is_(None))
            .order_by(OutboxEvent.occurred_at)
            .limit(limit)
        )
        events = result.scalars().all()
        published = 0

        for event in events:
            event.attempt_count += 1
            payload = json.loads(event.payload)
            if not isinstance(payload, dict):
                continue
            self.publisher.publish(
                event_type=event.event_type,
                payload=payload,
                deduplication_key=str(event.id),
            )
            event.published_at = datetime.now(UTC)
            published += 1

        await self.session.commit()
        return published