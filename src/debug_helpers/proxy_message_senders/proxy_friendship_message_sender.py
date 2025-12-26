import logging

from typing import Callable

from src.domain.message_senders import IFriendshipMessageSender

class ProxyFriendshipMessageSender(IFriendshipMessageSender):


    def __init__(self,
                 real_message_sender: IFriendshipMessageSender,
                 fake_message_sender: IFriendshipMessageSender,
                 reality_predicate: Callable[[int], bool]):
        self._real_message_sender = real_message_sender
        self._fake_message_sender = fake_message_sender
        self._reality_predicate = reality_predicate
        self._logger = logging.getLogger(__name__)

    async def send_friendship_request(self, id_from: int, id_to: int, name_from: str) -> bool:
        if self._reality_predicate(id_to):
            return await self._real_message_sender.send_friendship_request(id_from, id_to, name_from)
        self._logger.info(f'Сообщение пользователю {id_to} направлено на fake sender')
        return await self._fake_message_sender.send_friendship_request(id_from, id_to, name_from)

    async def send_friendship_accepted(self, id_accepted: int, id_requested: int, name_accepted: str) -> bool:
        if self._reality_predicate(id_requested):
            return await self._real_message_sender.send_friendship_accepted(id_accepted, id_requested, name_accepted)
        self._logger.info(f'Сообщение пользователю {id_requested} направлено на fake sender')
        return await self._fake_message_sender.send_friendship_accepted(id_accepted, id_requested, name_accepted)
