from abc import ABC, abstractmethod

from src.domain.dto.responses.fq import SendFqStatus, ResponseFqStatus


class IFqService(ABC):
    @abstractmethod
    async def send_fq(self, id_from: int, id_to: int) -> SendFqStatus:
        pass

    @abstractmethod
    async def response_fq(self, id_from: int, id_to: int) -> ResponseFqStatus:
        pass
