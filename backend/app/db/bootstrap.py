from app.core.config import get_settings
from app.db.base import Base
from app.db.session import engine
import app.models  # noqa: F401


async def bootstrap_local_database() -> None:
    settings = get_settings()
    if settings.app_env != 'local' or not settings.resolved_database_url.startswith('sqlite'):
        return
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)