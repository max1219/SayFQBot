from dataclasses import dataclass

@dataclass(slots=True)
class Friendship:
    user1_id: int
    user2_id: int