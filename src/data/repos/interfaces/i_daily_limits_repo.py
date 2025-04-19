from abc import ABC, abstractmethod

from ...entities import DailyLimits, User

class IDayLimitsRepo(ABC):
    @abstractmethod
    def get_by_user(self, user: User) -> DailyLimits:
        pass

    @abstractmethod
    def get_by_username(self, username: str) -> User:
        pass

    @abstractmethod
    def add(self, daily_limits: DailyLimits) -> None:
        pass

    @abstractmethod
    def remove(self, daily_limits: DailyLimits) -> None:
        pass

    @abstractmethod
    def edit(self, daily_limits: DailyLimits) -> None:
        pass
