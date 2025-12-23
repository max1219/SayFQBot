import asyncio

from typing import List, Tuple

from src.domain.repositories import IFriendshipRequestRepo


class InMemoryFriendshipRequestRepo(IFriendshipRequestRepo):
    def __init__(self, lock: asyncio.Lock):
        self._pairs: List[Tuple[int, int]] = []
        self._lock = lock

    def get_lock(self) -> asyncio.Lock:
        return self._lock

    async def add_request(self, user1_id: int, user2_id: int) -> None:
        self._pairs.append((user1_id, user2_id))

    async def remove_request(self, user1_id: int, user2_id: int, ignore_order: bool) -> None:
        self._pairs.remove((user1_id, user2_id))
        if ignore_order:
            self._pairs.remove((user2_id, user1_id))

    async def is_exists(self, user1_id: int, user2_id: int, ignore_order: bool) -> bool:
        return (user1_id, user2_id) in self._pairs or ignore_order and (user2_id, user1_id) in self._pairs
