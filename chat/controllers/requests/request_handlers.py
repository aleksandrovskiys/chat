import asyncio
import logging

from chat.controllers.messages.message_controller import MessageController
from chat.schemas.request import (
    LoginRequestModel,
    LogoutRequestModel,
    MessageRequestModel,
    RequestModel,
    RequestType,
)
from chat.schemas.response import ResponseModel, ResponseType
from chat.storage.storage import get_user_storage

logger = logging.getLogger(__name__)


class BaseRequestHandler[Model: RequestModel]:
    request_type: RequestType

    def __init__(self, request: Model) -> None:
        if request.type != self.request_type:
            raise ValueError(
                f"Invalid request type {request.type}. "
                f"Expected {self.request_type}"
            )

        self.request = request

    def handle(self) -> None:
        raise NotImplementedError

    def _send_response(self, response: ResponseModel) -> None:
        asyncio.create_task(
            self.request.connection.send_json(response.model_dump())
        )


class LoginRequestHandler(BaseRequestHandler[LoginRequestModel]):
    request_type = RequestType.LOGIN

    def handle(self):
        username = self.request.data.username
        storage = get_user_storage()

        user = storage.add_user(username, connection=self.request.connection)

        self._send_login_message(username, user.id)

        self._send_response(
            ResponseModel(
                data=user.model_dump(),
                message="Successful login",
                code=0,
                response_type=ResponseType.SUCCESSFUL_LOGIN,
            )
        )

    def _send_login_message(self, username: str, user_id: int) -> None:
        storage = get_user_storage()
        message_controller = MessageController(storage)

        asyncio.create_task(
            message_controller.send_message(
                message=f"{username} joined the chat",
                author_id=user_id,
            )
        )


class MessageRequestHandler(BaseRequestHandler[MessageRequestModel]):
    request_type = RequestType.MESSAGE

    def handle(self):
        self._send_message()
        self._send_response(
            ResponseModel(
                message="Message sent",
                code=0,
                response_type=ResponseType.MESSAGE_SENT,
            )
        )

    def _send_message(self) -> None:
        storage = get_user_storage()
        user = storage.get_by_connection(self.request.connection)

        if user is None:
            raise ValueError("User not found")

        message_controller = MessageController(storage)
        asyncio.create_task(
            message_controller.send_message(
                message=self.request.data.message,
                author_id=user.id,
            )
        )


class LogoutRequestHandler(BaseRequestHandler[LogoutRequestModel]):
    request_type = RequestType.LOGOUT

    def handle(self):
        storage = get_user_storage()
        user = storage.get_by_connection(self.request.connection)

        if user is None:
            raise ValueError("User not found")

        storage.remove_user(user.id)

        message_controller = MessageController(storage)
        asyncio.create_task(
            message_controller.send_message(
                message=f"{user.username} left the chat",
                author_id=user.id,
            )
        )
        logger.info(f"User {user.username} disconnected")

        self._send_response(
            ResponseModel(
                message="Successful logout",
                code=0,
                response_type=ResponseType.SUCCESSFUL_LOGIN,
                data=user.model_dump(),
            )
        )


class FallbackRequestHandler(BaseRequestHandler):
    request_type = RequestType.UNKNOWN

    def handle(self):
        self._send_response(
            ResponseModel(
                message="Unknown request type",
                code=1,
                response_type=ResponseType.UNKNOWN_REQUEST_TYPE,
            )
        )
