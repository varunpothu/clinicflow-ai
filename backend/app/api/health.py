from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.dependencies import get_session

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/live")
def liveness() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/ready")
async def readiness(session: AsyncSession = Depends(get_session)) -> dict[str, str]:
    await session.execute(text("SELECT 1"))
    return {"status": "ready"}
