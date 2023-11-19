from datetime import timedelta
import asyncpg
from demo_app.db.models.database_base import Database
from demo_app.db.models.measurement import Measurement, MeasurementAverage
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
        raise NotImplementedError
