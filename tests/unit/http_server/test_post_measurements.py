from fastapi.testclient import TestClient


def post_measurement_without_body_should_respond_with_422(test_client: TestClient):
    response = test_client.post("/measurements/someroom")
    assert response.status_code == 422
