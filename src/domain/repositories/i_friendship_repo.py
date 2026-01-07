from abc import abstractmethod, ABC
from typing import Sequence



class IFriendshipRepo(ABC):
    @abstractmethod
    async def check_friendship(self, user1_id: int, user2_id: int) -> bool:
        pass

    @abstractmethod
    async def get_all_friends(self, user_id: int) -> Sequence[int]:
        pass

    @abstractmethod
    async def add_friendship(self, user1_id: int, user2_id: int) -> None:
        pass

    @abstractmethod
    async def try_remove_friendship(self, user1_id: int, user2_id: int) -> bool:
        pass