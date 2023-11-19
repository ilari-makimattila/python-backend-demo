from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends
from demo_app.db.models.database_base import Database
from demo_app.db.models.measurement import Measurement, Unit
from demo_app.http_server.dependencies import get_database
from demo_app.http_server.dto_base_model import DTOBaseModel

router = APIRouter(
    prefix="/measurements",
)


class CreateMeasurementDTO(DTOBaseModel):
    v: float | int
    u: str = "K"
    ts: datetime


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
    m = Measurement(
        room_id=room_id,
        value=measurement.v,
        unit=Unit.K,
        timestamp=measurement.ts,
    )
    if database.insert_measurement(m):
        return
