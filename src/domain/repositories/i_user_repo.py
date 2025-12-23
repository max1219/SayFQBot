from abc import abstractmethod
from typing import Optional

from src.domain.entities import User
from src.domain.repositories.i_repo import IRepo


class IUserRepo(IRepo):
    @abstractmethod
    async def is_exists(self, user_id: int) -> bool:
        pass

    @abstractmethod
    async def get_by_name(self, name: str) -> Optional[User]:
        pass

    @abstractmethod
    async def get_by_id(self, user_id: int) -> Optional[User]:
        pass

    @abstractmethod
    async def add_user(self, user: User) -> None:
        pass