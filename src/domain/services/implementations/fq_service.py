from src.domain.repositories import IFriendshipRepo, IUserRepo, IFqRepo
from src.domain.message_senders import IFqMessageSender
from src.domain.dto.responses.fq import SendFqStatus
from src.domain.services import IFqService, IFqLimitsService


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

        async with self._fq_repo.get_lock():
            limits_availability: IFqLimitsService.LimitsExceeds = await self._limits_service.is_available(id_from, id_to)

            if IFqLimitsService.LimitsExceeds.TotalLimitExceeded in limits_availability:
                return SendFqStatus.TotalLimitExceeded

            if IFqLimitsService.LimitsExceeds.ToThisFriendLimitExceeded in limits_availability:
                return SendFqStatus.ToThisFriendLimitExceeded

            name_from = (await self._user_repo.get_by_id(id_from)).name

            if await self._message_sender.send_fq(id_from, id_to, name_from):
                await self._fq_repo.add_fq(id_from, id_to)
                return SendFqStatus.Success
            else:
                return SendFqStatus.CannotSendMessage
