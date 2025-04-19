from abc import ABC, abstractmethod

from ...entities import User

class IUserRepo(ABC):
    @abstractmethod
    async def get_by_id(self, user_id: int) -> User:
        pass

    @abstractmethod
    async def get_by_username(self, username: str) -> User:
        pass

    @abstractmethod
    async def add(self, user: User) -> None:
        pass

    @abstractmethod
    async def remove(self, user: User) -> None:
        pass

    @abstractmethod
    async def edit(self, user: User) -> None:
        pass
