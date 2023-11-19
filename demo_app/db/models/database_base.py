from abc import ABC

from demo_app.db.models.measurement import Measurement


class Database(ABC):
    def insert_measurement(self, measurement: Measurement) -> bool:
        """Store a measurement in the database"""
        raise NotImplementedError
