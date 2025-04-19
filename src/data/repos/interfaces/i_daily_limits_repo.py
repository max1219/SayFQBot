from abc import ABC, abstractmethod
from typing import Optional

from ...entities import DailyLimits, User

class IDayLimitsRepo(ABC):
    @abstractmethod
    async def get_by_user(self, user: User) -> Optional[DailyLimits]:
        pass

    @abstractmethod
    async def add(self, daily_limits: DailyLimits) -> None:
        pass

    @abstractmethod
    async def remove(self, daily_limits: DailyLimits) -> None:
        pass

    @abstractmethod
    async def edit(self, daily_limits: DailyLimits) -> None:
        pass
