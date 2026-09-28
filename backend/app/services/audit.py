from uuid import UUID

from app.domain.audit import AuditEvent


class AuditLog:
    def __init__(self) -> None:
        self._events: list[AuditEvent] = []

    def record(self, event: AuditEvent) -> AuditEvent:
        self._events.append(event)
        return event

    def for_entity(self, entity_id: UUID) -> list[AuditEvent]:
        return [event for event in self._events if event.entity_id == entity_id]

    def recent(self, limit: int = 100) -> list[AuditEvent]:
        return list(reversed(self._events[-limit:]))
