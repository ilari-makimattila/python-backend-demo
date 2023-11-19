from datetime import datetime

from fastapi import APIRouter
from demo_app.http_server.dto_base_model import DTOBaseModel

router = APIRouter(
    prefix="/measurements",
)


class CreateMeasurementDTO(DTOBaseModel):
    v: float | int
    u: str = "K"
    ts: datetime


@router.post("/{room_id}")
async def create_measurement(
    room_id: str,
    measurement: CreateMeasurementDTO,
) -> None:
    return
