from dataclasses import dataclass
from datetime import UTC, datetime


@dataclass
class PendingOutboxEvent:
    event_id: str
    event_type: str
    payload: str
    attempts: int = 0
    published_at: datetime | None = None


class OutboxPublisher:
    def publish(self, event: PendingOutboxEvent) -> str:
        event.attempts += 1
        event.published_at = datetime.now(UTC)
        return "PUBLISHED"
