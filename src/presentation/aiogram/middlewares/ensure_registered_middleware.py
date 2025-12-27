import logging
from typing import Callable, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User

from src.domain.services import IUserService
from src.domain.dto.requests.user import AddUserRequest


class EnsureRegisteredMiddleware(BaseMiddleware):
    def __init__(self):
        self._logger = logging.getLogger(__name__)

    async def __call__(self, handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]], event: TelegramObject,
                       data: dict[str, Any]) -> Any:
        user: User = data.get("event_from_user")

        if user is None:
            return await handler(event, data)

        user_id = user.id
        user_service: IUserService = data.get("user_service")

        if not await user_service.is_exists(user_id):
            await user_service.add_user(AddUserRequest(user_id=user_id, name=user.username))
            self._logger.info(f"User {user_id} был добавлен")

        return await handler(event, data)
