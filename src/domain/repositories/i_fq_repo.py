from abc import abstractmethod, ABC

from .operation_results import AddFqStatus


class IFqRepo(ABC):
    @abstractmethod
    async def try_add_fq(self, id_from: int, id_to: int, limit_total: int, limit_to:int) -> AddFqStatus:
        pass

    @abstractmethod
    async def remove_fq(self, id_from: int, id_to: int) -> None:
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