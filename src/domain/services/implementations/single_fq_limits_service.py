from src.domain.repositories import IFqRepo

from src.domain.services import IFqLimitsService
from src.domain.services.interfaces.i_total_fq_limit_provider import ITotalFqLimitProvider


class SingleFqLimitsService(IFqLimitsService):



    def __init__(self,
                 total_fq_limit_provider: ITotalFqLimitProvider,
                 fq_repo: IFqRepo):
        self._total_fq_limit_provider = total_fq_limit_provider
        self._fq_repo = fq_repo

    async def is_available(self, id_from: int, id_to: int) -> IFqLimitsService.LimitsExceeds:
        result: IFqLimitsService.LimitsExceeds = IFqLimitsService.LimitsExceeds(0)

        if await self.get_total_limit_spent(id_from) >= await self.get_total_limit(id_from):
            result |= IFqLimitsService.LimitsExceeds.TotalLimitExceeded

        if await self.get_to_this_friend_limit_spent(id_from, id_to) >= await self.get_to_this_friend_limit(id_from, id_to):
            result |= IFqLimitsService.LimitsExceeds.ToThisFriendLimitExceeded

        return result


    async def get_total_limit(self, user_id: int) -> int:
        return await self._total_fq_limit_provider.get_fq_limit(user_id)

    async def get_total_limit_spent(self, user_id: int) -> int:
        return await self._fq_repo.get_total_sent_count(user_id)

    async def get_to_this_friend_limit(self, id_from: int, id_to: int) -> int:
        return 1

    async def get_to_this_friend_limit_spent(self, id_from: int, id_to: int) -> int:
        return await self._fq_repo.get_to_this_friend_sent_count(id_from, id_to)

    async def clear_spent_limits(self) -> None:
        await self._fq_repo.clear()

