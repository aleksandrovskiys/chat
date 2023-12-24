from fastapi.websockets import WebSocket
from pydantic import BaseModel, Field
from pydantic.config import ConfigDict


class User(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: int
    username: str
    connection: WebSocket = Field(..., exclude=True)


class Test:
    ...
