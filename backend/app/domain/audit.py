from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import UUID, uuid4


@dataclass(frozen=True)
class AuditEvent:
    event_id: UUID
    event_type: str
    actor_id: UUID | None
    workflow_id: UUID | None
    entity_id: UUID | None
    correlation_id: str
    occurred_at: datetime
    summary: str
    metadata: dict[str, str]

    @classmethod
    def create(
        cls,
        *,
        event_type: str,
        correlation_id: str,
        summary: str,
        actor_id: UUID | None = None,
        workflow_id: UUID | None = None,
        entity_id: UUID | None = None,
        metadata: dict[str, str] | None = None,
    ) -> "AuditEvent":
        return cls(
            event_id=uuid4(),
            event_type=event_type,
            actor_id=actor_id,
            workflow_id=workflow_id,
            entity_id=entity_id,
            correlation_id=correlation_id,
            occurred_at=datetime.now(UTC),
            summary=summary,
            metadata=metadata or {},
        )
