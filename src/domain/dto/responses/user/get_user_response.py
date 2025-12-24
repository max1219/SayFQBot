from dataclasses import dataclass

@dataclass(slots=True, frozen=True)
class GetUserResponse:
    user_id: int
    name: str