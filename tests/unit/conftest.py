import pytest
from unittest.mock import Mock
from fastapi.testclient import TestClient


@pytest.fixture()
def database():
    return Mock()


@pytest.fixture()
def app():
    import demo_app.http_server.app
    return demo_app.http_server.app


@pytest.fixture()
def test_client(app):
    return TestClient(app)
