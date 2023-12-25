import logging

from fastapi.routing import APIRouter
from fastapi.websockets import WebSocket, WebSocketDisconnect
from pydantic.type_adapter import TypeAdapter

from chat.controllers.requests.requests import handle_request
from chat.schemas.request import LogoutRequestModel, RequestModel

router = APIRouter(prefix="/websocket")

logger = logging.getLogger(__name__)


@router.websocket("/ws")
async def websocket_route(ws: WebSocket):
    await ws.accept()
    while True:
        try:
            data = await ws.receive_json()
            data["connection"] = ws

            adapter = TypeAdapter(RequestModel)
            request = adapter.validate_python(data)

            response = handle_request(request)
            await ws.send_json(response.model_dump())
        except WebSocketDisconnect:
            data = LogoutRequestModel(connection=ws)
            response = handle_request(data)
            logging.info(f"User {response.data["username"]} disconnected")
            return
