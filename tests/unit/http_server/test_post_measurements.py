from datetime import datetime
from unittest.mock import Mock
from zoneinfo import ZoneInfo
from fastapi.testclient import TestClient


def post_measurement_without_body_should_respond_with_422(test_client: TestClient):
    response = test_client.post("/measurements/someroom")
    assert response.status_code == 422


def post_measurement_should_store_measurement(test_client: TestClient, database: Mock):
    database.insert_measurement.return_value = True
    response = test_client.post("/measurements/myroom", json={"v": 300, "u": "K", "ts": "2023-11-19T12:00:00Z"})
    assert response.status_code == 201
    database.insert_measurement.assert_called_once_with(
        Measurement("myroom", 300, "K", datetime(2023, 19, 11, 12, 0, 0, 0, tzinfo=ZoneInfo("UTC"))),
    )
