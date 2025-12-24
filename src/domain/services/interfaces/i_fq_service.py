from abc import ABC, abstractmethod

from src.domain.dto.responses.fq import SendFqStatus


class IFqService(ABC):
    @abstractmethod
    async def send_fq(self, id_from: int, id_to: int) -> SendFqStatus:
        pass

    # Нужен ли?
    # @abstractmethod
    # def resend_fq(self, id_from: int, id_to: int) -> SendFqStatus:
    #     pass
