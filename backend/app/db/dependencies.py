from collections.abc import AsyncIterator

from app.db.session import SessionLocal


async def get_session() -> AsyncIterator[object]:
    async with SessionLocal() as session:
        yield session
