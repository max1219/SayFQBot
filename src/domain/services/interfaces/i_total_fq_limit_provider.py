from abc import ABC, abstractmethod

class ITotalFqLimitProvider(ABC):
    @abstractmethod
    async def get_fq_limit(self, user_id: int) -> int:
        pass