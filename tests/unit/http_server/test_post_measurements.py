from datetime import datetime
from unittest.mock import Mock
from zoneinfo import ZoneInfo
from fastapi.testclient import TestClient
from pydantic import ValidationError
import pytest

from demo_app.db.models.measurement import Measurement, MeasurementAverage, Unit
from demo_app.http_server.routes.measurements import CreateMeasurementDTO


def post_measurement_without_body_should_respond_with_422(test_client: TestClient):
    response = test_client.post("/measurements/someroom")
    assert response.status_code == 422


def post_measurement_should_store_measurement(test_client: TestClient, database: Mock):
    database.insert_measurement.return_value = True
    response = test_client.post("/measurements/myroom", json={"v": 300, "u": "K", "ts": "2023-11-19T12:00:00Z"})
    assert response.status_code == 201
    database.insert_measurement.assert_called_once_with(
        Measurement(
            room_id="myroom",
            value=300,
            unit=Unit.K,
            timestamp=datetime(2023, 11, 19, 12, 0, 0, 0, tzinfo=ZoneInfo("UTC")),
        ),
    )


def post_measurement_should_default_to_k(test_client: TestClient, database: Mock):
    database.insert_measurement.return_value = True
    response = test_client.post("/measurements/aroom", json={"v": 20, "ts": "2023-11-19T13:00:00Z"})
    assert response.status_code == 201
    database.insert_measurement.assert_called_once_with(
        Measurement(
            room_id="aroom",
            value=20,
            unit=Unit.K,
            timestamp=datetime(2023, 11, 19, 13, 0, 0, 0, tzinfo=ZoneInfo("UTC")),
        ),
    )


def post_measurement_should_return_501_if_measurement_unit_is_not_k(test_client: TestClient, database: Mock):
    response = test_client.post("/measurements/myroom", json={"v": 300, "u": "C", "ts": "2023-11-19T12:00:00Z"})
    assert response.status_code == 501
    database.insert_measurement.assert_not_called()


def post_measurement_should_return_422_if_measurement_value_is_impossible(test_client: TestClient, database: Mock):
    response = test_client.post("/measurements/myroom", json={"v": -100, "ts": "2023-11-19T12:00:00Z"})
    assert response.status_code == 422
    body = response.json()
    assert "Kelvin value must be greater than or equal to 0" in body["detail"][0]["msg"]
    database.insert_measurement.assert_not_called()


def create_measurement_dto_should_not_allow_negative_kelvin():
    with pytest.raises(ValidationError) as e:
        CreateMeasurementDTO(v=-100, u="K", ts=datetime(2023, 11, 19, 12, 0, 0, 0, tzinfo=ZoneInfo("UTC")))
    assert "Kelvin value must be greater than or equal to 0" in str(e.value)


def get_measurement_average_should_return_404_if_room_is_not_found(test_client: TestClient, database: Mock):
    database.get_room_average.return_value = None
    response = test_client.get("/measurements/myroom/average/PT5M")
    assert response.status_code == 404


def get_measurement_average_should_return_422_if_duration_is_invalid(test_client: TestClient, database: Mock):
    database.get_room_average.return_value = None
    response = test_client.get("/measurements/myroom/average/foo")
    assert response.status_code == 422


def get_measurement_average_should_return_the_average(test_client: TestClient, database: Mock):
    database.get_room_average.return_value = MeasurementAverage(
        value=320.0,
        unit=Unit.K,
        interval_start_timestamp=datetime(2023, 11, 19, 12, 5, 0, 0, tzinfo=ZoneInfo("UTC")),
        interval_end_timestamp=datetime(2023, 11, 19, 12, 10, 0, 0, tzinfo=ZoneInfo("UTC")),
        measurement_count=3,
    )
    response = test_client.get("/measurements/myroom/average/PT5M")
    assert response.status_code == 200
    assert response.json().items() >= {
        "v": 320.0,
        "u": "K",
        "ts": "2023-11-19T12:05:00Z"
    }.items()
