import logging

from typing import Callable

from src.domain.message_senders import IFqMessageSender

class ProxyFqMessageSender(IFqMessageSender):
    def __init__(self,
                 real_message_sender: IFqMessageSender,
                 fake_message_sender: IFqMessageSender,
                 reality_predicate: Callable[[int], bool]):
        self._real_message_sender = real_message_sender
        self._fake_message_sender = fake_message_sender
        self._reality_predicate = reality_predicate
        self._logger = logging.getLogger(__name__)

    async def send_fq(self, id_from: int, id_to: int, name_from: str) -> bool:
        if self._reality_predicate(id_to):
            return await self._real_message_sender.send_fq(id_from, id_to, name_from)
        self._logger.info(f'Сообщение пользователю {id_to} направлено на fake sender')
        return await self._fake_message_sender.send_fq(id_from, id_to, name_from)