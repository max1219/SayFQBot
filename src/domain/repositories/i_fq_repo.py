from abc import abstractmethod

from src.domain.repositories.i_repo import IRepo


class IFqRepo(IRepo):
    @abstractmethod
    async def add_fq(self, id_from: int, id_to: int) -> None:
        pass

    @abstractmethod
    async def clear(self) -> None:
        pass

    @abstractmethod
    async def get_total_sent_count(self, id_from: int) -> int:
        pass

    @abstractmethod
    async def get_to_this_friend_sent_count(self, id_from: int, id_to: int) -> int:
        pass