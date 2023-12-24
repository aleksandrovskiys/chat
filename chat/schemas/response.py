from enum import Enum

from pydantic import BaseModel


class ResponseType(str, Enum):
    SUCCESSFUL_LOGIN = "Successful login"
    UNSUCCESSFUL_LOGIN = "Unsuccessful login"
    MESSAGE_SENT = "Message sent"

    UNKNOWN_REQUEST_TYPE = "Unknown request type"


class ResponseModel(BaseModel):
    message: str
    code: int
    response_type: ResponseType
    data: dict = {}
