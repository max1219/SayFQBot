import logging

from aiogram import Bot
from aiogram.exceptions import AiogramError

from src.domain.message_senders import IFqMessageSender
from src.domain.services.presentation import LexiconBase

from src.presentation.aiogram.keyboards.inline import create_response_fq_kb


class AiogramFqMessageSender(IFqMessageSender):
    def __init__(self, bot: Bot, lexicon: LexiconBase):
        self._bot = bot
        self._lexicon = lexicon
        self._logger = logging.getLogger(__name__)

    async def send_fq(self, id_from: int, id_to: int, name_from: str) -> bool:
        try:
            await self._bot.send_message(
                chat_id=id_to,
                text=self._lexicon.get('fq').format(name_from=name_from),
                reply_markup=create_response_fq_kb(id_from, self._lexicon))
            return True
        except AiogramError:
            self._logger.warning(f'Не удалось отправить fq для "{id_to}".', exc_info=True)
            return False

    async def response_fq(self, id_from: int, id_to: int, name_from: str) -> bool:
        try:
            text = self._lexicon.get('fq_resp_pattern').format(
                name_from=name_from,
                text=self._lexicon.get('fq_resp')
            )
            await self._bot.send_message(
                chat_id=id_to,
                text=text)
            return True
        except AiogramError:
            self._logger.warning(f'Не удалось отправить fq для "{id_to}".', exc_info=True)
            return False
