from starlette.testclient import WebSocketTestSession

from chat.storage.storage import get_user_storage


def test_login(websocket_session: WebSocketTestSession):
    username = "test_user_name"
    websocket_session.send_json(
        {"type": "login", "data": {"username": username}}
    )
    response = websocket_session.receive_json()
    assert response is not None
    assert response["message"] == "Successful login"
    assert response["code"] == 0
    assert "data" in response
    assert isinstance(response["data"], dict)
    assert "username" in response["data"]
    assert response["data"]["username"] == username
    assert "id" in response["data"]
    user_id = response["data"]["id"]
    assert isinstance(user_id, int)
    assert "connection" not in response["data"]

    storage = get_user_storage()

    user = storage.get_user(user_id)
    assert user is not None
    assert user.id == user_id
    assert user.username == username
