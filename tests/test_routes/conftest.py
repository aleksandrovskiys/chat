from typing import Generator, TypeVar

import pytest
from fastapi.testclient import TestClient
from starlette.testclient import WebSocketTestSession

from chat.app import app

T = TypeVar("T")

YieldFixture = Generator[T, None, None]


@pytest.fixture(scope="session")
def test_client() -> TestClient:
    client = TestClient(app)
    return client


@pytest.fixture()
def websocket_session(
    test_client: TestClient,
) -> YieldFixture[WebSocketTestSession]:
    with test_client.websocket_connect("/websocket/ws") as connection:
        yield connection
