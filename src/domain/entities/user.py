from dataclasses import dataclass

@dataclass(slots=True, frozen=True)
class User:
    user_id: int
    name: str
