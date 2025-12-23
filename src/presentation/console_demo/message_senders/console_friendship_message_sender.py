from src.domain.message_senders import IFriendshipMessageSender


class ConsoleFriendshipMessageSender(IFriendshipMessageSender):
    async def send_friendship_request(self, id_from: int, id_to: int, name_from: str) -> bool:
        print(f"### For {id_to}. Friendship requested from: {name_from}")
        return True

    async def send_friendship_accepted(self, id_accepted: int, id_requested: int, name_accepted: str) -> bool:
        print(f"### For {id_requested}. Friendship accepted from: {name_accepted}")
        return True