from abc import ABC
from datetime import timedelta

from demo_app.db.models.measurement import Measurement


class Database(ABC):
    def insert_measurement(self, measurement: Measurement) -> bool:
        """Store a measurement in the database"""
        raise NotImplementedError

    def get_room_average(self, room_id: str, duration: timedelta) -> float:
        """Get the average temperature of a room for a given duration"""
        raise NotImplementedError
