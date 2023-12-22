import pytest
from fastapi.testclient import TestClient

from chat.app import app


@pytest.fixture(scope="session")
def test_client() -> TestClient:
    client = TestClient(app)
    return client
