import logging

from aiogram import Bot
from aiogram.exceptions import AiogramError

from src.domain.message_senders import IFqMessageSender


class AiogramFqMessageSender(IFqMessageSender):
    def __init__(self, bot: Bot):
        self._bot = bot
        self._logger = logging.getLogger(__name__)

    async def send_fq(self, id_from: int, id_to: int, name_from: str) -> bool:
        try:
            await self._bot.send_message(chat_id=id_to, text=f'Пашел нахуй от {name_from}')
            return True
        except AiogramError:
            self._logger.warning(f'Не удалось отправить fq для "{id_to}".', exc_info=True)
            return False