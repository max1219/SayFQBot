from abc import abstractmethod

from src.domain.repositories.i_repo import IRepo


class IFriendshipRequestRepo(IRepo):
    @abstractmethod
    async def add_request(self, user1_id: int, user2_id: int) -> None:
        pass

    @abstractmethod
    async def remove_request(self, user1_id: int, user2_id: int, ignore_order: bool) -> None:
        pass

    @abstractmethod
    async def is_exists(self, user1_id: int, user2_id: int, ignore_order: bool) -> bool:
        pass