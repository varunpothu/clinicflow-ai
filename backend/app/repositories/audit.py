import json
from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.audit import AuditEventRecord


class AuditRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def record(
        self,
        *,
        event_type: str,
        summary: str,
        correlation_id: str,
        actor_id: UUID | None = None,
        workflow_id: UUID | None = None,
        entity_id: UUID | None = None,
        metadata: dict[str, str] | None = None,
        occurred_at: datetime,
    ) -> AuditEventRecord:
        event = AuditEventRecord(
            id=str(uuid4()),
            event_type=event_type,
            actor_id=str(actor_id) if actor_id else None,
            workflow_id=str(workflow_id) if workflow_id else None,
            entity_id=str(entity_id) if entity_id else None,
            correlation_id=correlation_id,
            summary=summary,
            metadata_json=json.dumps(metadata or {}, sort_keys=True),
            occurred_at=occurred_at,
        )
        self.session.add(event)
        await self.session.flush()
        return event
