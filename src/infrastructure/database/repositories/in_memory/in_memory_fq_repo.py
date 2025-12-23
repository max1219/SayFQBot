import asyncio

from typing import List, Tuple

from src.domain.repositories import IFqRepo


class InMemoryFqRepo(IFqRepo):
    def __init__(self, lock: asyncio.Lock):
        self._pairs: List[Tuple[int, int]] = list()
        self._lock = lock

    def get_lock(self) -> asyncio.Lock:
        return self._lock

    async def add_fq(self, id_from: int, id_to: int) -> None:
        self._pairs.append((id_from, id_to))

    async def clear(self) -> None:
        self._pairs.clear()

    async def get_total_sent_count(self, id_from: int) -> int:
        return sum(1 for _, _ in
                   filter(lambda pair: pair[0] == id_from, self._pairs))

    async def get_to_this_friend_sent_count(self, id_from: int, id_to: int) -> int:
        return sum(1 for _, _ in
                   filter(lambda pair: pair[0] == id_from and pair[1] == id_to, self._pairs))