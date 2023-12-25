from chat.controllers.requests.request_handlers import (
    BaseRequestHandler,
    FallbackRequestHandler,
    LoginRequestHandler,
    LogoutRequestHandler,
    MessageRequestHandler,
)
from chat.schemas.request import RequestModel


def get_handler_for_request(request: RequestModel) -> BaseRequestHandler:
    match request.type:
        case LoginRequestHandler.request_type:
            return LoginRequestHandler(request)  # type: ignore
        case MessageRequestHandler.request_type:
            return MessageRequestHandler(request)  # type: ignore
        case LogoutRequestHandler.request_type:
            return LogoutRequestHandler(request)  # type: ignore
        case _:
            return FallbackRequestHandler(request)


def handle_request(request: RequestModel) -> None:
    handler = get_handler_for_request(request)
    return handler.handle()
