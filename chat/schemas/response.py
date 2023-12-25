from enum import Enum

from pydantic import BaseModel


class ResponseType(str, Enum):
    SUCCESSFUL_LOGIN = "successful_login"
    UNSUCCESSFUL_LOGIN = "unsuccessful_login"

    MESSAGE = "message"
    MESSAGE_SENT = "message_sent"

    UNKNOWN_REQUEST_TYPE = "Unknown request type"


class ResponseModel(BaseModel):
    message: str
    code: int
    response_type: ResponseType
    data: dict = {}
