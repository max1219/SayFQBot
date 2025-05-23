from abc import ABC, abstractmethod
from typing import Tuple

from . import IUserRepo, IFriendshipRepo, IFriendshipRequestRepo, IDayLimitsRepo

class IDatabase(ABC):
    @abstractmethod
    async def init(self) -> Tuple[IUserRepo, IFriendshipRepo, IFriendshipRequestRepo, IDayLimitsRepo]:
        pass