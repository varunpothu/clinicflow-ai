import json
from datetime import UTC, datetime
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.idempotency import IdempotencyKey


class PersistentIdempotencyRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self, key: str) -> IdempotencyKey | None:
        result = await self.session.execute(
            select(IdempotencyKey).where(IdempotencyKey.key == key)
        )
        return result.scalar_one_or_none()

    async def put(self, key: str, fingerprint: str, result: dict[str, Any]) -> IdempotencyKey:
        record = IdempotencyKey(
            key=key,
            fingerprint=fingerprint,
            result_json=json.dumps(result, sort_keys=True, default=str),
            created_at=datetime.now(UTC),
        )
        self.session.add(record)
        await self.session.flush()
        return record
