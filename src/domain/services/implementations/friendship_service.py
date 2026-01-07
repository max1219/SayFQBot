import asyncio

from typing import Sequence

from src.domain.repositories import IFriendshipRepo, IFriendshipRequestRepo, IUserRepo
from src.domain.dto.responses.friendship import RequestFriendshipStatus, AcceptFriendshipStatus
from src.domain.message_senders import IFriendshipMessageSender

from src.domain.services import IFriendshipService


class FriendshipService(IFriendshipService):
    def __init__(self,
                 friendship_repo: IFriendshipRepo,
                 friendship_request_repo: IFriendshipRequestRepo,
                 user_repo: IUserRepo,
                 message_sender: IFriendshipMessageSender, ):
        self._friendship_repo = friendship_repo
        self._friendship_request_repo = friendship_request_repo
        self._user_repo = user_repo
        self._message_sender = message_sender
        self._lock = asyncio.Lock()

    async def get_all_friends(self, user_id: int) -> Sequence[int]:
        return await self._friendship_repo.get_all_friends(user_id)

    async def accept_friendship(self, id_accepted: int, id_requested: int) -> AcceptFriendshipStatus:
        is_exists: bool = await self._friendship_request_repo.try_remove_request(id_requested, id_accepted, False)
        if not is_exists:
            return AcceptFriendshipStatus.NotFound

        await self._friendship_repo.add_friendship(id_requested, id_accepted)
        name_accepted = (await self._user_repo.get_by_id(id_accepted)).name
        await self._message_sender.send_friendship_accepted(id_accepted, id_requested, name_accepted)
        return AcceptFriendshipStatus.Success

    async def request_friendship_by_name(self, id_from: int, name_to: str) -> RequestFriendshipStatus:
        user_to = await self._user_repo.get_by_name(name_to)
        if user_to is None:
            return RequestFriendshipStatus.UserNotFound

        id_to = user_to.user_id
        return await self.request_friendship_by_id(id_from, id_to)

    async def request_friendship_by_id(self, id_from: int, id_to: int) -> RequestFriendshipStatus:

        async with self._lock:
            if not await self._user_repo.is_exists(id_to):
                return RequestFriendshipStatus.UserNotFound

            is_auto_accepted = (await self.accept_friendship(id_from, id_to)) == AcceptFriendshipStatus.Success
            if is_auto_accepted:
                return RequestFriendshipStatus.AutoAccepted

            if await self._friendship_repo.check_friendship(id_from, id_to):
                return RequestFriendshipStatus.AlreadyFriend

            is_exists = not await self._friendship_request_repo.try_add_request(id_from, id_to)
            if is_exists:
                return RequestFriendshipStatus.AlreadyRequested

            name_from = (await self._user_repo.get_by_id(id_from)).name
        is_sent = await self._message_sender.send_friendship_request(id_from, id_to, name_from)
        if is_sent:
            return RequestFriendshipStatus.Success
        await self._friendship_request_repo.try_remove_request(id_from, id_to, False)
        return RequestFriendshipStatus.CannotSendMessage

    async def remove_friendship(self, user1_id: int, user2_id: int) -> bool:
        return await self._friendship_repo.try_remove_friendship(user1_id, user2_id)

    async def get_incoming_requests(self, user_to_id: int) -> Sequence[int]:
        return await self._friendship_request_repo.get_incoming_requests(user_to_id)
