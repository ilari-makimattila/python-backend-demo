from datetime import datetime
from enum import StrEnum
from pydantic import BaseModel


class Unit(StrEnum):
    """Temperature unit"""
    K = "K"
    C = "C"
    F = "F"


class Measurement(BaseModel):
    """Representation of one temperature measurement"""
    room_id: str
    value: float
    unit: Unit
    timestamp: datetime


class MeasurementAverage(BaseModel):
    """Representation of one temperature measurement between an interval"""
    value: float | int
    unit: Unit
    interval_start_timestamp: datetime
    interval_end_timestamp: datetime
