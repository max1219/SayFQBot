from abc import ABC, abstractmethod
from typing import Sequence

from ...entities import FriendshipRequest, Friendship, User

class IFriendshipRequestRepo(ABC):
    @abstractmethod
    def get_unordered(self, friendship: Friendship) -> FriendshipRequest:
        pass

    @abstractmethod
    def get_all_incoming(self, user: User) -> Sequence[FriendshipRequest]:
        pass

    @abstractmethod
    def add(self, friendship_request: FriendshipRequest) -> None:
        pass

    @abstractmethod
    def remove(self, friendship_request: FriendshipRequest) -> None:
        pass

    @abstractmethod
    def expire(self, user: User) -> int:
        pass

