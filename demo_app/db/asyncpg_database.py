from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import asyncpg
from demo_app.db.models.database_base import Database
from demo_app.db.models.measurement import Measurement, MeasurementAverage, Unit
from demo_app.settings import Settings


class NotConnectedError(Exception):
    pass

class AsyncpgDatabase(Database):
    def __init__(
        self,
        settings: Settings,
        connection: asyncpg.Connection | None = None,  # type: ignore # (asyncpg stub claims it's generic but it's not)
    ):
        self.settings = settings
        self.conn = connection

    async def connect(self) -> None:
        if self.conn is not None:
            return
        self.conn = await asyncpg.connect(self.settings.database_dsn)

    async def migrate(self) -> None:
        if self.conn is None:
            raise NotConnectedError()

        # TODO better migrations
        await self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS measurements (
                room_id TEXT,
                timestamp_ns BIGINT,
                value FLOAT,
                unit TEXT,
                PRIMARY KEY (room_id, timestamp_ns)
            )
            """,
        )

    async def insert_measurement(self, measurement: Measurement) -> bool:
        if self.conn is None:
            raise NotConnectedError()

        result = await self.conn.execute(
            """
            INSERT INTO measurements
            VALUES ($1, $2, $3, $4)
            """,
            measurement.room_id,
            measurement.timestamp.timestamp() * 1_000_000_000,
            measurement.value,
            measurement.unit,
        )
        return not not result

    async def get_room_average(self, room_id: str, duration: timedelta) -> MeasurementAverage | None:
        if self.conn is None:
            raise NotConnectedError()
        result = await self.conn.fetch(
            """
            SELECT
                AVG(value) AS value,
                MIN(timestamp_ns) AS interval_start_timestamp,
                MAX(timestamp_ns) AS interval_end_timestamp,
                COUNT(*) AS count
            FROM measurements
            WHERE room_id = $1
            AND timestamp_ns >= $2
            """,
            room_id,
            (datetime.utcnow() - duration).timestamp() * 1_000_000_000,
        )
        if len(result) == 0 or result[0]["count"] == 0:
            return None
        print(result)
        return MeasurementAverage(
            value=result[0]["value"],
            unit=Unit.K,
            interval_start_timestamp=datetime.fromtimestamp(
                result[0]["interval_start_timestamp"] / 1_000_000_000, tz=ZoneInfo("UTC"),
            ),
            interval_end_timestamp=datetime.fromtimestamp(
                result[0]["interval_end_timestamp"] / 1_000_000_000, tz=ZoneInfo("UTC"),
            ),
            measurement_count=result[0]["count"],
        )
