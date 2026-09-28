from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class IdempotencyRecord:
    key: str
    fingerprint: str
    result: Any


class IdempotencyStore:
    def __init__(self) -> None:
        self._records: dict[str, IdempotencyRecord] = {}

    def get(self, key: str) -> IdempotencyRecord | None:
        return self._records.get(key)

    def put(self, key: str, fingerprint: str, result: Any) -> IdempotencyRecord:
        record = IdempotencyRecord(key=key, fingerprint=fingerprint, result=result)
        self._records[key] = record
        return record
