from typing import Sequence

from src.domain.repositories import IFriendshipRepo, IFriendshipRequestRepo, IUserRepo
from src.domain.dto.responces.friendship import RequestFriendshipStatus, AcceptFriendshipStatus
from src.domain.message_senders import IFriendshipMessageSender

from src.domain.services import IFriendshipService

class FriendshipService(IFriendshipService):
    def __init__(self,
                 friendship_repo: IFriendshipRepo,
                 friendship_request_repo: IFriendshipRequestRepo,
                 user_repo: IUserRepo,
                 message_sender: IFriendshipMessageSender,):
        self._friendship_repo = friendship_repo
        self._friendship_request_repo = friendship_request_repo
        self._user_repo = user_repo
        self._message_sender = message_sender

    async def get_all_friends(self, user_id: int) -> Sequence[int]:
        return await self._friendship_repo.get_all_friends(user_id)

    async def accept_friendship(self, id_accepted: int, id_requested: int) -> AcceptFriendshipStatus:
        async with self._friendship_request_repo.get_lock():
            if await self._friendship_request_repo.is_exists(id_requested, id_accepted, False):
                await self._friendship_request_repo.remove_request(id_requested, id_accepted, False)
                await self._friendship_repo.add_friendship(id_requested, id_accepted)
                name_accepted = (await self._user_repo.get_by_id(id_accepted)).name
                await self._message_sender.send_friendship_accepted(id_accepted, id_requested, name_accepted)
                return AcceptFriendshipStatus.Success
            return AcceptFriendshipStatus.NotFound


    async def request_friendship(self, id_from: int, name_to: str) -> RequestFriendshipStatus:
        user_to = await self._user_repo.get_by_name(name_to)
        if user_to is None:
            return RequestFriendshipStatus.UserNotFound

        id_to = user_to.user_id

        async with self._friendship_request_repo.get_lock():
            if await self._friendship_request_repo.is_exists(id_from, id_to, False):
                return RequestFriendshipStatus.AlreadyRequested

            if await self._friendship_request_repo.is_exists(id_to, id_from, False):
                await self.accept_friendship(id_from, id_to)
                return RequestFriendshipStatus.AutoAccepted

            if await self._friendship_repo.check_friendship(id_from, id_to):
                return RequestFriendshipStatus.AlreadyFriend

            name_from = (await self._user_repo.get_by_id(id_from)).name
            is_sent = await self._message_sender.send_friendship_request(id_from, id_to, name_from)
            if is_sent:
                await self._friendship_request_repo.add_request(id_from, id_to)
                return RequestFriendshipStatus.Success

            return RequestFriendshipStatus.CannotSendMessage

    async def remove_friendship(self, user1_id: int, user2_id: int) -> bool:
        async with self._friendship_repo.get_lock():
            if not self._friendship_repo.check_friendship(user1_id, user2_id):
                return False

            await self._friendship_repo.remove_friendship(user1_id, user2_id)
            return True