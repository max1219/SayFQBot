from dataclasses import dataclass

@dataclass(slots=True, frozen=True)
class Friendship:
    user1_id: int
    user2_id: int