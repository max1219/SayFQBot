from dataclasses import dataclass

@dataclass(slots=True, frozen=True)
class User:
    id: int
    username: str
    n_friends: int