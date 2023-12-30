from fastapi.routing import APIRouter
from fastapi.websockets import WebSocket, WebSocketDisconnect
from pydantic.type_adapter import TypeAdapter

from chat.controllers.requests.requests import handle_request
from chat.schemas.request import LogoutRequestModel, RequestModel

router = APIRouter(prefix="/websocket")


@router.websocket("/ws")
async def websocket_route(ws: WebSocket):
    await ws.accept()
    while True:
        try:
            data = await ws.receive_json()
            data["connection"] = ws

            adapter = TypeAdapter(RequestModel)
            request = adapter.validate_python(data)

            handle_request(request)
        except WebSocketDisconnect:
            data = LogoutRequestModel(connection=ws)
            handle_request(data)
            return
