import asyncio

from typing import Optional, List

from src.domain.repositories import IUserRepo
from src.domain.entities import User


class InMemoryUserRepo(IUserRepo):
    def __init__(self, lock: asyncio.Lock):
        self._users: List[User] = []
        self._lock = lock

    def get_lock(self) -> asyncio.Lock:
        return self._lock

    async def add_user(self, user: User) -> None:
        self._users.append(user)

    async def is_exists(self, user_id: int) -> bool:
        return any(map(lambda user: user.user_id == user_id, self._users))

    async def get_by_name(self, name: str) -> Optional[int]:
        result = next(filter(lambda user: user.name == name, self._users), None)
        if result is None:
            return None
        else:
            return result

    async def get_by_id(self, user_id: int) -> Optional[str]:
        result = next(filter(lambda user: user.user_id == user_id, self._users), None)
        if result is None:
            return None
        else:
            return result


