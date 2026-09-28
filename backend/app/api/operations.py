from fastapi import APIRouter

from app.services.audit import AuditLog
from app.services.exceptions import ExceptionQueue

router = APIRouter(prefix="/operations", tags=["operations"])

audit_log = AuditLog()
exception_queue = ExceptionQueue()


@router.get("/audit")
def get_recent_audit(limit: int = 50) -> list[dict[str, object]]:
    return [
        {
            "event_id": str(event.event_id),
            "event_type": event.event_type,
            "occurred_at": event.occurred_at.isoformat(),
            "summary": event.summary,
            "correlation_id": event.correlation_id,
            "metadata": event.metadata,
        }
        for event in audit_log.recent(limit)
    ]


@router.get("/exceptions")
def get_open_exceptions() -> list[dict[str, object]]:
    return [
        {
            "exception_id": str(item.exception_id),
            "code": item.code,
            "severity": item.severity,
            "status": item.status,
            "summary": item.summary,
            "created_at": item.created_at.isoformat(),
            "retry_count": item.retry_count,
        }
        for item in exception_queue.list_open()
    ]
