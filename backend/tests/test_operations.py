from uuid import uuid4

from app.domain.audit import AuditEvent
from app.domain.exceptions import ExceptionSeverity, OperationalException
from app.services.audit import AuditLog
from app.services.exceptions import ExceptionQueue


def test_audit_log_preserves_recent_events() -> None:
    log = AuditLog()
    first = log.record(
        AuditEvent.create(
            event_type="PROPOSAL_CREATED",
            correlation_id="corr-1",
            summary="Proposal created",
            entity_id=uuid4(),
        )
    )
    second = log.record(
        AuditEvent.create(
            event_type="APPROVAL_REQUESTED",
            correlation_id="corr-1",
            summary="Approval requested",
            entity_id=first.entity_id,
        )
    )
    assert log.recent(1)[0] == second
    assert log.for_entity(first.entity_id)[0] == first


def test_exception_queue_lists_unresolved_items() -> None:
    queue = ExceptionQueue()
    item = queue.add(
        OperationalException.create(
            code="BOOKING_CONFLICT",
            severity=ExceptionSeverity.HIGH,
            summary="Slot was taken",
            correlation_id="corr-2",
        )
    )
    assert queue.list_open() == [item]
