from abc import ABC, abstractmethod
from typing import Sequence

from ...entities import FriendshipRequest, Friendship, User

class IFriendshipRequestRepo(ABC):
    @abstractmethod
    async def get_unordered(self, friendship: Friendship) -> FriendshipRequest:
        pass

    @abstractmethod
    async def get_all_incoming(self, user: User) -> Sequence[FriendshipRequest]:
        pass

    @abstractmethod
    async def add(self, friendship_request: FriendshipRequest) -> None:
        pass

    @abstractmethod
    async def remove(self, friendship_request: FriendshipRequest) -> None:
        pass

    @abstractmethod
    async def expire(self, user: User) -> int:
        pass

