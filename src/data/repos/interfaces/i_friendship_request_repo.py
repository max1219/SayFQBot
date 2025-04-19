from abc import ABC, abstractmethod
from typing import Iterable, Optional

from ...entities import FriendshipRequest, Friendship, User

class IFriendshipRequestRepo(ABC):
    @abstractmethod
    async def get_unordered(self, friendship: Friendship) -> Optional[FriendshipRequest]:
        pass

    @abstractmethod
    async def get_all_incoming(self, user: User) -> Iterable[FriendshipRequest]:
        pass

    @abstractmethod
    async def add(self, friendship_request: FriendshipRequest) -> int:
        pass

    @abstractmethod
    async def remove(self, friendship_request: FriendshipRequest) -> None:
        pass

    @abstractmethod
    async def cleanup(self) -> int:
        pass

