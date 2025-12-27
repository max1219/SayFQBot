from typing import Any

from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery

from src.presentation.aiogram.services import IsAdminService


class IsAdminFilter(BaseFilter):
    async def __call__(
            self, update: Message | CallbackQuery, is_admin_service: IsAdminService) -> bool | dict[str, Any]:
        return is_admin_service.check(update.from_user.id)
