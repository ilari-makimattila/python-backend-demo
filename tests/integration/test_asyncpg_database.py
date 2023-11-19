import random
import asyncpg
from datetime import datetime
from faker import Faker
from zoneinfo import ZoneInfo
from demo_app.db.asyncpg_database import AsyncpgDatabase
from demo_app.db.models.measurement import Measurement, Unit

fake = Faker()

async def asyncpg_database_should_insert_measurement(connection: asyncpg.Connection, asyncpg_database: AsyncpgDatabase):
    m = Measurement(
        room_id=fake.name(),
        value=random.randint(0, 100),
        unit=Unit.K,
        timestamp=datetime(2023, 11, 19, 12, 0, 0, 0, tzinfo=ZoneInfo("UTC")),
    )
    assert await asyncpg_database.insert_measurement(m)
    data = await connection.fetch(
        "SELECT * FROM measurements WHERE room_id = $1 AND value = $2 AND unit = $3",
        m.room_id,
        m.value,
        m.unit,
    )
    assert len(data) == 1
    assert data[0]["room_id"] == m.room_id
    assert data[0]["value"] == m.value
    assert data[0]["unit"] == m.unit
    assert data[0]["timestamp_ns"] == m.timestamp.timestamp() * 1_000_000_000
