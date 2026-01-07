from abc import abstractmethod, ABC
from typing import Optional, Sequence

from src.domain.entities import User


class IUserRepo(ABC):
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
    async def try_add_user(self, user: User) -> bool:
        pass

    @abstractmethod
    async def get_all_users(self) -> Sequence[User]:
        pass

    @abstractmethod
    async def remove_user(self, user_id: int) -> None:
        pass