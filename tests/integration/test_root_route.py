from fastapi.testclient import TestClient


def root_route_should_respond_with_200_ok(test_client: TestClient):
    response = test_client.get("/")
    assert response.status_code == 200
