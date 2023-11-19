import asyncpg
import pytest
from fastapi.testclient import TestClient
from demo_app.db.asyncpg_database import AsyncpgDatabase
from demo_app.http_server.dependencies import get_settings

from demo_app.settings import Settings


@pytest.fixture()
def settings() -> Settings:
    return Settings(
        database_dsn="postgresql://demo:password@localhost:54321/demo",  # assume docker postgres is up
    )


@pytest.fixture()
async def connection(settings: Settings):
    conn = await asyncpg.connect(settings.database_dsn)
    yield conn
    await conn.close()


@pytest.fixture()
async def asyncpg_database(settings: Settings, connection: asyncpg.Connection):
    db = AsyncpgDatabase(settings=settings, connection=connection)
    await db.migrate()
    return db


@pytest.fixture()
async def app(settings: Settings):
    from demo_app.http_server.app import app
    app.dependency_overrides[get_settings] = lambda: settings
    yield app
    app.dependency_overrides = {}


@pytest.fixture()
def test_client(app):
    return TestClient(app)
