from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fastapi.testclient import TestClient


def test_healthcheck(test_client: "TestClient"):
    response = test_client.get("/healthcheck")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
