import random
import asyncpg
from datetime import datetime, timedelta
from faker import Faker
from zoneinfo import ZoneInfo

from pytest import approx
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


async def asyncpg_database_should_return_none_if_nothing_is_found(asyncpg_database: AsyncpgDatabase):
    result = await asyncpg_database.get_room_average(room_id=fake.name(), duration=timedelta(minutes=10))
    assert result is None


async def asyncpg_database_should_retrieve_average(asyncpg_database: AsyncpgDatabase):
    room = fake.name()
    ts = datetime.utcnow().replace(tzinfo=ZoneInfo("UTC"))
    m1 = Measurement(room_id=room, value=300, unit=Unit.K, timestamp=ts + timedelta(minutes=0))
    m2 = Measurement(room_id=room, value=310, unit=Unit.K, timestamp=ts + timedelta(minutes=5))
    m3 = Measurement(room_id=room, value=320, unit=Unit.K, timestamp=ts + timedelta(minutes=9))
    await asyncpg_database.insert_measurement(m1)
    await asyncpg_database.insert_measurement(m2)
    await asyncpg_database.insert_measurement(m3)

    result = await asyncpg_database.get_room_average(room_id=room, duration=timedelta(minutes=10))
    assert result is not None
    assert result.interval_start_timestamp == approx(ts)
    assert result.value == 310
    assert result.unit == Unit.K
    assert result.measurement_count == 3
