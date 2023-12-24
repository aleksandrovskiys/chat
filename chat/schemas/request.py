from enum import Enum
from typing import Annotated, Literal, Union

from fastapi.websockets import WebSocket
from pydantic import BaseModel, Field
from pydantic.config import ConfigDict


class RequestType(str, Enum):
    LOGIN = "login"
    LOGOUT = "logout"
    MESSAGE = "message"

    UNKNOWN = "unknown"

    @classmethod
    def _missing_(cls, value: object) -> "RequestType":
        if isinstance(value, str):
            return cls.UNKNOWN
        raise ValueError(f"{value} is not a valid {cls.__name__}")


class BaseRequestModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    connection: WebSocket


class LoginRequestDataModel(BaseModel):
    username: str


class MessageRequestDataModel(BaseModel):
    message: str


class LoginRequestModel(BaseRequestModel):
    type: Literal[RequestType.LOGIN]
    data: LoginRequestDataModel


class MessageRequestModel(BaseRequestModel):
    type: Literal[RequestType.MESSAGE]
    data: MessageRequestDataModel


RequestModel = Annotated[
    Union[LoginRequestModel, MessageRequestModel],
    Field(..., discriminator="type"),
]
