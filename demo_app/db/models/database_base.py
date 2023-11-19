from abc import ABC
from datetime import timedelta

from demo_app.db.models.measurement import Measurement, MeasurementAverage


class Database(ABC):
    def insert_measurement(self, measurement: Measurement) -> bool:
        """Store a measurement in the database"""
        raise NotImplementedError

    def get_room_average(self, room_id: str, duration: timedelta) -> MeasurementAverage | None:
        """Get the average temperature of a room for a given duration.
           None is returned if no measurements are found."""
        raise NotImplementedError
