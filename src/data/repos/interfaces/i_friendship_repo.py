from abc import ABC, abstractmethod
from typing import Sequence

from ...entities import Friendship, User

class IFriendshipRepo(ABC):
    @abstractmethod
    def is_friends(self, friendship: Friendship) -> bool:
        pass

    @abstractmethod
    def get_all(self, user: User) -> Sequence[Friendship]:
        pass

    @abstractmethod
    def add(self, friendship: Friendship) -> None:
        pass

    @abstractmethod
    def remove(self, friendship: Friendship) -> None:
        pass