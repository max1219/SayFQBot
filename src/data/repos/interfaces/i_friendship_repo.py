from abc import ABC, abstractmethod
from typing import Iterable, Optional

from ...entities import Friendship, User

class IFriendshipRepo(ABC):
    @abstractmethod
    async def get_unordered(self, friendship: Friendship) -> Optional[Friendship]:
        pass

    @abstractmethod
    async def get_all(self, user: User) -> Iterable[Friendship]:
        pass

    @abstractmethod
    async def add(self, friendship: Friendship) -> None:
        pass

    @abstractmethod
    async def remove(self, friendship: Friendship) -> None:
        pass