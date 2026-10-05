from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import get_settings
from app.db.bootstrap import bootstrap_local_database
from app.observability import CorrelationIdMiddleware, configure_logging


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    configure_logging(get_settings().log_level)
    await bootstrap_local_database()
    yield


def create_app() -> FastAPI:
    settings = get_settings()
    application = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        description="Human-in-the-loop clinic appointment orchestration platform.",
        lifespan=lifespan,
    )
    application.add_middleware(CorrelationIdMiddleware)
    application.include_router(api_router)
    return application


app = create_app()
