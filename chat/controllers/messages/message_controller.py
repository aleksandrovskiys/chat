import asyncio

from chat.schemas.response import ResponseModel, ResponseType
from chat.storage.users import UserStorage


class MessageController:
    def __init__(self, user_storage: UserStorage):
        self._storage = user_storage

    async def send_message(
        self, message: str, author_id: int, reciever_id: int | None = None
    ):
        if reciever_id is None:
            users = self._storage.get_all_users()
        else:
            user = self._storage.get_user(reciever_id)
            if user is None:
                raise ValueError(f"User with id {reciever_id} not found")

            users = [user]

        for user in users:
            response = ResponseModel(
                message=message,
                code=0,
                response_type=ResponseType.MESSAGE,
                data={},
            )
            asyncio.create_task(
                user.connection.send_json(response.model_dump())
            )
