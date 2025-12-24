from dataclasses import dataclass

@dataclass(slots=True, frozen=True)
class AddUserRequest:
    user_id: int
    name: str