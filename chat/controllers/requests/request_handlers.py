from chat.schemas.request import (
    LoginRequestModel,
    MessageRequestModel,
    RequestModel,
    RequestType,
)
from chat.schemas.response import ResponseModel, ResponseType
from chat.storage.storage import get_user_storage


class BaseRequestHandler[Model: RequestModel]:
    request_type: RequestType

    def __init__(self, request: Model) -> None:
        if request.type != self.request_type:
            raise ValueError(
                f"Invalid request type {request.type}. "
                f"Expected {self.request_type}"
            )

        self.request = request

    def handle(self) -> ResponseModel:
        raise NotImplementedError


class LoginRequestHandler(BaseRequestHandler[LoginRequestModel]):
    request_type = RequestType.LOGIN

    def handle(self) -> ResponseModel:
        username = self.request.data.username
        storage = get_user_storage()

        user = storage.add_user(username, connection=self.request.connection)

        return ResponseModel(
            data=user.model_dump(),
            message="Successful login",
            code=0,
            response_type=ResponseType.SUCCESSFUL_LOGIN,
        )


class MessageRequestHandler(BaseRequestHandler[MessageRequestModel]):
    request_type = RequestType.MESSAGE

    def handle(self) -> ResponseModel:
        return ResponseModel(
            message="Message sent",
            code=0,
            response_type=ResponseType.MESSAGE_SENT,
        )


class FallbackRequestHandler(BaseRequestHandler):
    request_type = RequestType.UNKNOWN

    def handle(self) -> ResponseModel:
        return ResponseModel(
            message="Unknown request type",
            code=1,
            response_type=ResponseType.UNKNOWN_REQUEST_TYPE,
        )
