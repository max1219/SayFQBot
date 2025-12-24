from abc import ABC, abstractmethod
from typing import Optional

from src.domain.dto.responses.user import GetUserResponse
from src.domain.dto.requests.user import AddUserRequest


class IUserService(ABC):
    @abstractmethod
    async def is_exists(self, user_id: int) -> bool:
        pass

    @abstractmethod
    async def get_by_name(self, name: str) -> Optional[GetUserResponse]:
        pass

    @abstractmethod
    async def get_by_id(self, user_id: int) -> Optional[GetUserResponse]:
        pass

    @abstractmethod
    async def add_user(self, request: AddUserRequest) -> None:
        pass