from src.domain.repositories import IFriendshipRepo, IUserRepo, IFqRepo
from src.domain.message_senders import IFqMessageSender
from src.domain.dto.responses.fq import SendFqStatus
from src.domain.services import IFqService, IFqLimitsService
from src.domain.repositories.operation_results import AddFqStatus


class FqService(IFqService):
    def __init__(self,
                 message_sender: IFqMessageSender,
                 friendship_repo: IFriendshipRepo,
                 user_repo: IUserRepo,
                 limits_service: IFqLimitsService,
                 fq_repo: IFqRepo, ):
        self._message_sender = message_sender
        self._friendship_repo = friendship_repo
        self._user_repo = user_repo
        self._limits_service = limits_service
        self._fq_repo = fq_repo

    async def send_fq(self, id_from: int, id_to: int) -> SendFqStatus:
        if not await self._user_repo.is_exists(id_to):
            return SendFqStatus.UserNotFound

        if not await self._friendship_repo.check_friendship(id_from, id_to):
            return SendFqStatus.NotFriend

        limit_total = await self._limits_service.get_total_limit(id_from)
        limit_to = await self._limits_service.get_to_this_friend_limit(id_from, id_to)
        add_fq_status: AddFqStatus = await self._fq_repo.try_add_fq(id_from, id_to, limit_total, limit_to)

        if AddFqStatus.TotalLimitExceeded in add_fq_status:
            return SendFqStatus.TotalLimitExceeded
        if AddFqStatus.ToThisFriendLimitExceeded in add_fq_status:
            return SendFqStatus.ToThisFriendLimitExceeded


        name_from = (await self._user_repo.get_by_id(id_from)).name

        if await self._message_sender.send_fq(id_from, id_to, name_from):
            return SendFqStatus.Success
        else:
            await self._fq_repo.remove_fq(id_from, id_to)
            return SendFqStatus.CannotSendMessage
