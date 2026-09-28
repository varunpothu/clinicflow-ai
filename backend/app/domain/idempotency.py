from dataclasses import dataclass
from typing import Generic, TypeVar


T = TypeVar("T")


@dataclass(frozen=True)
class IdempotencyRecord(Generic[T]):
    key: str
    fingerprint: str
    result: T


class IdempotencyStore(Generic[T]):
    def __init__(self) -> None:
        self._records: dict[str, IdempotencyRecord[T]] = {}

    def get(self, key: str) -> IdempotencyRecord[T] | None:
        return self._records.get(key)

    def put(self, key: str, fingerprint: str, result: T) -> IdempotencyRecord[T]:
        record = IdempotencyRecord(key=key, fingerprint=fingerprint, result=result)
        self._records[key] = record
        return record
