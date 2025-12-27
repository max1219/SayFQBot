from dataclasses import dataclass

@dataclass(slots=True, frozen=True)
class FriendEntry:
    user_id: int
    name: str
    is_already_sent: bool

@dataclass(slots=True, frozen=True)
class PaginationData:
    current_page: int
    total_pages: int