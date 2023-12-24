from abc import ABC, abstractmethod

from fastapi.websockets import WebSocket

from chat.schemas.user import User


class UserStorage(ABC):
    @abstractmethod
    def add_user(self, username: str, connection: WebSocket) -> User:
        ...

    @abstractmethod
    def remove_user(self, id: int) -> User:
        ...

    @abstractmethod
    def get_user(self, id: int) -> User:
        ...

    @abstractmethod
    def get_all_users(self) -> list[User]:
        ...

    @abstractmethod
    def get_all_usernames(self) -> list[str]:
        ...

    @abstractmethod
    def get_all_user_connections(self) -> list[WebSocket]:
        ...

    @abstractmethod
    def __len__(self) -> int:
        ...


class InMemoryUserStorage(UserStorage):
    def __init__(self):
        self.users: list[User] = []

    def add_user(self, username: str, connection: WebSocket) -> User:
        user = User(
            id=len(self.users),
            username=username,
            connection=connection,
        )
        self.users.append(user)
        return user

    def remove_user(self, id: int) -> User:
        user = self.get_user(id)
        self.users.remove(user)
        return user

    def get_user(self, id: int) -> User:
        return self.users[id]

    def get_all_users(self) -> list[User]:
        return self.users

    def get_all_usernames(self) -> list[str]:
        return [user.username for user in self.users]

    def get_all_user_connections(self) -> list[WebSocket]:
        return [user.connection for user in self.users]

    def __len__(self) -> int:
        return len(self.users)
