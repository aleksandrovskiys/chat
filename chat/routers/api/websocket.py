from fastapi.routing import APIRouter
from fastapi.websockets import WebSocket, WebSocketDisconnect
from pydantic.type_adapter import TypeAdapter

from chat.controllers.requests.requests import handle_request
from chat.schemas.request import RequestModel

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

            response = handle_request(request)
            await ws.send_json(response.model_dump())
        except WebSocketDisconnect as e:
            # TODO: handle disconnect, remove user from users list
            print(e)
            break
