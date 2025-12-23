import asyncio

from typing import Sequence, List, Tuple

from src.domain.repositories import IFriendshipRepo


class InMemoryFriendshipRepo(IFriendshipRepo):
    def __init__(self, lock: asyncio.Lock):
        self._pairs: List[Tuple[int, int]] = list()
        self._lock = lock

    def get_lock(self) -> asyncio.Lock:
        return self._lock

    async def check_friendship(self, user1_id, user2_id) -> bool:
        return (user1_id, user2_id) in self._pairs or (user2_id, user1_id) in self._pairs

    async def get_all_friends(self, user_id) -> Sequence[int]:
        return list(map(lambda pair: pair[0] if pair[1] == user_id else pair[1],
                        filter(lambda pair: user_id in pair, self._pairs)))

    async def add_friendship(self, user1_id: int, user2_id: int) -> None:
        self._pairs.append((user1_id, user2_id))

    async def remove_friendship(self, user1_id: int, user2_id: int) -> None:
        self._pairs.remove((user1_id, user2_id))