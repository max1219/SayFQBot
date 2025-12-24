from src.domain.services.interfaces.i_total_fq_limit_provider import ITotalFqLimitProvider

class ConstantFqLimitProvider(ITotalFqLimitProvider):
    def __init__(self, limit: int):
        self._limit = limit

    async def get_fq_limit(self, user_id: int) -> int:
        return self._limit