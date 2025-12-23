from abc import ABC, abstractmethod
from enum import Flag


class IFqLimitsService(ABC):
    class LimitsExceeds(Flag):
        TotalLimitExceeded = 1
        ToThisFriendLimitExceeded = 2

    @abstractmethod
    async def is_available(self, id_from: int, id_to: int) -> LimitsExceeds:
        pass

    @abstractmethod
    async def get_total_limit(self, user_id: int) -> int:
        pass

    @abstractmethod
    async def get_to_this_friend_limit(self, id_from: int, id_to: int) -> int:
        pass

    @abstractmethod
    async def get_total_limit_spent(self, user_id: int) -> int:
        pass

    @abstractmethod
    async def get_to_this_friend_limit_spent(self, id_from: int, id_to: int) -> int:
        pass