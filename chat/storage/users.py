from abc import ABC, abstractmethod
from collections import deque
from typing import Sequence

from fastapi.websockets import WebSocket

from chat.schemas.user import User


class UserStorage(ABC):
    @abstractmethod
    def add_user(self, username: str, connection: WebSocket) -> User:
        ...

    @abstractmethod
    def remove_user(self, id: int) -> User | None:
        ...

    @abstractmethod
    def get_user(self, id: int) -> User | None:
        ...

    @abstractmethod
    def get_by_connection(self, connection: WebSocket) -> User | None:
        ...

    @abstractmethod
    def get_all_users(self) -> Sequence[User]:
        ...

    @abstractmethod
    def get_all_usernames(self) -> Sequence[str]:
        ...

    @abstractmethod
    def get_all_user_connections(self) -> Sequence[WebSocket]:
        ...

    @abstractmethod
    def __len__(self) -> int:
        ...


class InMemoryUserStorage(UserStorage):
    def __init__(self):
        self._users: deque[User] = deque()

    def add_user(self, username: str, connection: WebSocket) -> User:
        user = User(
            id=len(self._users),
            username=username,
            connection=connection,
        )
        self._users.append(user)
        return user

    def remove_user(self, id: int) -> User:
        user = self.get_user(id)
        if user is None:
            raise ValueError(f"User with id {id} not found")

        self._users.remove(user)
        return user

    def get_user(self, id: int) -> User | None:
        for user in self._users:
            if user.id == id:
                return user

    def get_by_connection(self, connection: WebSocket) -> User | None:
        for user in self._users:
            if user.connection == connection:
                return user

    def get_all_users(self) -> deque[User]:
        return self._users

    def get_all_usernames(self) -> list[str]:
        return [user.username for user in self._users]

    def get_all_user_connections(self) -> list[WebSocket]:
        return [user.connection for user in self._users]

    def __len__(self) -> int:
        return len(self._users)
