from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum
from uuid import UUID, uuid4


class ExceptionSeverity(StrEnum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class ExceptionStatus(StrEnum):
    OPEN = "OPEN"
    ACKNOWLEDGED = "ACKNOWLEDGED"
    RESOLVED = "RESOLVED"


@dataclass
class OperationalException:
    exception_id: UUID
    code: str
    severity: ExceptionSeverity
    status: ExceptionStatus
    summary: str
    workflow_id: UUID | None
    correlation_id: str
    created_at: datetime
    retry_count: int = 0
    resolution_note: str | None = None

    @classmethod
    def create(
        cls,
        *,
        code: str,
        severity: ExceptionSeverity,
        summary: str,
        correlation_id: str,
        workflow_id: UUID | None = None,
    ) -> "OperationalException":
        return cls(
            exception_id=uuid4(),
            code=code,
            severity=severity,
            status=ExceptionStatus.OPEN,
            summary=summary,
            workflow_id=workflow_id,
            correlation_id=correlation_id,
            created_at=datetime.now(UTC),
        )
