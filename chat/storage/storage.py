from chat.storage.users import InMemoryUserStorage, UserStorage

_user_storage: UserStorage | None = None


def get_user_storage() -> UserStorage:
    global _user_storage

    if not _user_storage:
        _user_storage = InMemoryUserStorage()

    return _user_storage
