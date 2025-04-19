from abc import ABC, abstractmethod
from typing import Sequence

from ...entities import Friendship, User

class IFriendshipRepo(ABC):
    @abstractmethod
    async def is_friends(self, friendship: Friendship) -> bool:
        pass

    @abstractmethod
    async def get_all(self, user: User) -> Sequence[Friendship]:
        pass

    @abstractmethod
    async def add(self, friendship: Friendship) -> None:
        pass

    @abstractmethod
    async def remove(self, friendship: Friendship) -> None:
        pass