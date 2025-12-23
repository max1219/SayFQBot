from abc import ABC, abstractmethod

class IFriendshipMessageSender(ABC):
    @abstractmethod
    async def send_friendship_request(self, id_from: int, id_to: int, name_from: str) -> bool:
        pass

    @abstractmethod
    async def send_friendship_accepted(self, id_accepted: int, id_requested: int, name_accepted: str) -> bool:
        pass