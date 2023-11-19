import pytest
from unittest.mock import Mock
from fastapi.testclient import TestClient

from demo_app.db.models.database_base import Database
from demo_app.http_server.dependencies import get_database


@pytest.fixture()
def database():
    return Mock(spec_set=Database)


@pytest.fixture()
def app(database: Mock):
    from demo_app.http_server.app import app
    app.dependency_overrides[get_database] = lambda: database
    yield app
    app.dependency_overrides = {}


@pytest.fixture()
def test_client(app):
    return TestClient(app)
