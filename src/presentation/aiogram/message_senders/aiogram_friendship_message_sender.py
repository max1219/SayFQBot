import logging

from aiogram import Bot
from aiogram.exceptions import AiogramError

from src.domain.message_senders import IFriendshipMessageSender

from src.presentation.aiogram.keyboards.inline import create_okay_kb, create_friendship_accept_kb


class AiogramFriendshipMessageSender(IFriendshipMessageSender):
    def __init__(self, bot: Bot):
        self._bot = bot
        self._logger = logging.getLogger(__name__)

    async def send_friendship_request(self, id_from: int, id_to: int, name_from: str) -> bool:
        try:
            await self._bot.send_message(
                chat_id=id_to,
                text=f'Вам приглашение в друзья от @{name_from}',
                reply_markup=create_friendship_accept_kb(id_from))
            return True
        except AiogramError:
            self._logger.warning(f'Не удалось отправить friendship request для "{id_to}".', exc_info=True)
            return False

    async def send_friendship_accepted(self, id_accepted: int, id_requested: int, name_accepted: str) -> bool:
        try:
            await self._bot.send_message(
                chat_id=id_requested,
                text=f'Теперь ты друг с {name_accepted}',
                reply_markup=create_okay_kb())
            return True
        except AiogramError:
            self._logger.warning(f'Не удалось отправить friendship accept для "{id_requested}".', exc_info=True)
            return False
