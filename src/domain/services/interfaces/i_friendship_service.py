from abc import ABC, abstractmethod
from typing import Sequence

from src.domain.dto.responses.friendship import AcceptFriendshipStatus, RequestFriendshipStatus

class IFriendshipService(ABC):
    @abstractmethod
    async def request_friendship_by_name(self, id_from: int, name_to: str) -> RequestFriendshipStatus:
        pass

    @abstractmethod
    async def request_friendship_by_id(self, id_from: int, id_to: int) -> RequestFriendshipStatus:
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

    @abstractmethod
    async def get_incoming_requests(self, user_to_id: int) -> Sequence[int]:
        pass