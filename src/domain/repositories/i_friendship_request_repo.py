from abc import abstractmethod, ABC
from typing import Sequence


class IFriendshipRequestRepo(ABC):
    @abstractmethod
    async def try_add_request(self, user1_id: int, user2_id: int) -> bool:
        pass

    @abstractmethod
    async def try_remove_request(self, user1_id: int, user2_id: int, ignore_order: bool) -> bool:
        pass

    @abstractmethod
    async def is_exists(self, user1_id: int, user2_id: int, ignore_order: bool) -> bool:
        pass

    @abstractmethod
    async def get_incoming_requests(self, user_to_id: int) -> Sequence[int]:
        pass
