from dataclasses import dataclass

@dataclass(slots=True, frozen=True)
class FriendshipRequest:
    id: int
    user_from_id: int
    user_to_id: int