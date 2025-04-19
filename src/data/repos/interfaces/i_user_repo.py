from abc import ABC, abstractmethod

from ...entities import User

class IUserRepo(ABC):
    @abstractmethod
    def get_by_id(self, user_id: int) -> User:
        pass

    @abstractmethod
    def get_by_username(self, username: str) -> User:
        pass

    @abstractmethod
    def add(self, user: User) -> None:
        pass

    @abstractmethod
    def remove(self, user: User) -> None:
        pass

    @abstractmethod
    def edit(self, user: User) -> None:
        pass
