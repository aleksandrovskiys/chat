from unittest import mock

from starlette.testclient import WebSocketTestSession

from chat.storage.storage import get_user_storage


def test_login_response(websocket_session: WebSocketTestSession):
    username = "test_user_name"
    storage = get_user_storage()
    with mock.patch(
        "chat.controllers.requests.request_handlers."
        "LoginRequestHandler._send_login_message"
    ) as login_message_mock:
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

        user = storage.get_user(user_id)
        assert user is not None
        assert user.id == user_id
        assert user.username == username

        login_message_mock.assert_called_once_with(username, user.id)


def test_send_message_response(websocket_session: WebSocketTestSession):
    username = "test_user_name"
    with mock.patch(
        "chat.controllers.requests.request_handlers."
        "LoginRequestHandler._send_login_message"
    ):
        websocket_session.send_json(
            {"type": "login", "data": {"username": username}}
        )
        websocket_session.receive_json()

    with mock.patch(
        "chat.controllers.requests.request_handlers."
        "MessageRequestHandler._send_message"
    ) as send_message_mock:
        message = "test_message"
        websocket_session.send_json(
            {"type": "message", "data": {"message": message}}
        )

        response = websocket_session.receive_json()

        assert response is not None
        assert response["message"] == "Message sent"
        assert response["code"] == 0
        assert "data" in response
        assert isinstance(response["data"], dict)
        assert response["data"] == {}

        send_message_mock.assert_called_once()
