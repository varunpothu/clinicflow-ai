from contextvars import ContextVar
from uuid import uuid4

_CORRELATION_ID: ContextVar[str] = ContextVar("correlation_id", default="")


def get_correlation_id() -> str:
    return _CORRELATION_ID.get()


def set_correlation_id(value: str | None = None) -> str:
    correlation_id = value or str(uuid4())
    _CORRELATION_ID.set(correlation_id)
    return correlation_id
