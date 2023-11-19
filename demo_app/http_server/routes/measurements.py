from datetime import datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic import Field, model_validator
from demo_app.db.models.database_base import Database
from demo_app.db.models.measurement import Measurement, Unit
from demo_app.http_server.dependencies import get_database
from demo_app.http_server.dto_base_model import DTOBaseModel

router = APIRouter(
    prefix="/measurements",
)


class CreateMeasurementDTO(DTOBaseModel):
    """Create a new measurement"""
    v: float | int = Field(description="The value of the measurement, for example 300")
    u: str = Field(description="The unit of the measurement. At the moment only K is supported", default="K")
    ts: datetime = Field(description="The timestamp of the measurement")

    @model_validator(mode="after")
    def validate_kelvin(self) -> 'CreateMeasurementDTO':
        if self.u.upper() == "K" and self.v < 0:
            raise ValueError("Kelvin value must be greater than or equal to 0")
        return self


class RoomAverageTemperatureDTO(DTOBaseModel):
    """Get the average temperature of a room for a given duration"""
    v: float | int = Field(description="The average temperature of the room during the duration")
    u: str = Field(description="The unit of the temperature", default="K")
    ts: datetime = Field(description="The timestamp the beginning of the measurements in the duration")


@router.post(
    "/{room_id}",
    status_code=201,
    description="Store a single measurement for a room",
)
async def create_measurement(
    database: Annotated[Database, Depends(get_database)],
    room_id: str,
    measurement: CreateMeasurementDTO,
) -> None:
    if measurement.u != "K":
        raise HTTPException(status_code=501, detail="Only Kelvin is supported at the moment")
    m = Measurement(
        room_id=room_id,
        value=measurement.v,
        unit=Unit.K,
        timestamp=measurement.ts,
    )
    if database.insert_measurement(m):
        return
    else:
        # database error handling is out of scope
        return


@router.get(
    "/{room_id}/average/{duration}",
    response_model=RoomAverageTemperatureDTO,
    description="Get the average temperature of a room for a given duration",
)
async def get_room_average(
    database: Annotated[Database, Depends(get_database)],
    room_id: str,
    duration: timedelta,
) -> RoomAverageTemperatureDTO:
    result = database.get_room_average(room_id, duration)
    if result is None:
        raise HTTPException(status_code=404, detail="Room not found")
    return RoomAverageTemperatureDTO(
        v=result.value,
        u=result.unit,
        ts=result.interval_start_timestamp,
    )
