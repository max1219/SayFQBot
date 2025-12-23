from abc import ABC, abstractmethod
from typing import Sequence

from src.domain.dto.responces.friendship import AcceptFriendshipStatus, RequestFriendshipStatus

class IFriendshipService(ABC):
    @abstractmethod
    async def request_friendship(self, id_from: int, name_to: str) -> RequestFriendshipStatus:
        pass

    @abstractmethod
    async def accept_friendship(self, id_accepted: int, id_requested: int) -> AcceptFriendshipStatus:
        pass

    @abstractmethod
    async def get_all_friends(self, user_id: int) -> Sequence[int]:
        pass

    @abstractmethod
    async def remove_friendship(self, user1_id: int, user2_id: int) -> bool:
        pass