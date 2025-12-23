from src.domain.message_senders import IFqMessageSender

class ConsoleFqMessageSender(IFqMessageSender):
    async def send_fq(self, id_from: int, id_to: int, name_from: str) -> bool:
        print(f"### For {id_to}. Пашел нахуй от {name_from}")
        return True
