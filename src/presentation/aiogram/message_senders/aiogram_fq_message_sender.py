import logging

from aiogram import Bot
from aiogram.exceptions import AiogramError

from src.domain.message_senders import IFqMessageSender
from src.domain.services.presentation import LexiconBase

class AiogramFqMessageSender(IFqMessageSender):
    def __init__(self, bot: Bot, lexicon: LexiconBase):
        self._bot = bot
        self._lexicon = lexicon
        self._logger = logging.getLogger(__name__)

    async def send_fq(self, id_from: int, id_to: int, name_from: str) -> bool:
        try:
            await self._bot.send_message(
                chat_id=id_to,
                text=self._lexicon.get('fq').format(name_from=name_from))
            return True
        except AiogramError:
            self._logger.warning(f'Не удалось отправить fq для "{id_to}".', exc_info=True)
            return False