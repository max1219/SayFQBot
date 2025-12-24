from typing import Optional

from src.domain.dto.requests.user import AddUserRequest
from src.domain.dto.responses.user import GetUserResponse
from src.domain.entities import User
from src.domain.repositories import IUserRepo
from src.domain.services import IUserService

class UserService(IUserService):
    def __init__(self, user_repo: IUserRepo):
        self._user_repo = user_repo

    async def is_exists(self, user_id: int) -> bool:
        return await self._user_repo.is_exists(user_id)

    async def get_by_name(self, name: str) -> Optional[GetUserResponse]:
        user: Optional[User] = await self._user_repo.get_by_name(name)
        if user is None:
            return None
        return GetUserResponse(user_id=user.user_id, name=user.name)

    async def get_by_id(self, user_id: int) -> Optional[GetUserResponse]:
        user: Optional[User] = await self._user_repo.get_by_id(user_id)
        if user is None:
            return None
        return GetUserResponse(user_id=user.user_id, name=user.name)

    async def add_user(self, request: AddUserRequest) -> None:
        async with self._user_repo.get_lock():
            if await self._user_repo.is_exists(request.user_id):
                # Мб потом че поставить сюда
                pass
            await self._user_repo.add_user(User(user_id=request.user_id, name=request.name))