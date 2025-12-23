from abc import ABC, abstractmethod

class IFqMessageSender(ABC):
    @abstractmethod
    async def send_fq(self, id_from: int, id_to: int, name_from: str) -> bool:
        pass