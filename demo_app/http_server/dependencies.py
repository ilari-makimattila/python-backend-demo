from typing import Annotated

from fastapi import Depends
from demo_app.db.asyncpg_database import AsyncpgDatabase
from demo_app.db.models.database_base import Database
from demo_app.settings import Settings


def get_settings() -> Settings:
    return Settings()  # type: ignore # (pydantic settings can be initialized without parameters but mypy complains)


async def get_database(settings: Annotated[Settings, Depends(get_settings)]) -> Database:
    db = AsyncpgDatabase(settings)
    await db.connect()
    await db.migrate()
    return db
