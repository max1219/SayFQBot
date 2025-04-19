from abc import ABC, abstractmethod

from ...entities import DailyLimits, User

class IDayLimitsRepo(ABC):
    @abstractmethod
    async def get_by_user(self, user: User) -> DailyLimits:
        pass

    @abstractmethod
    async def get_by_username(self, username: str) -> User:
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
