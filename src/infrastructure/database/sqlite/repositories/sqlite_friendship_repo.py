import asyncio

from typing import Sequence

from src.domain.repositories import IFriendshipRepo
from src.infrastructure.database.sqlite.connection_pool import ConnectionPool
from src.infrastructure.database.sqlite.transaction_type import TransactionType


class SqliteFriendshipRepo(IFriendshipRepo):
    def __init__(self, connection_pool: ConnectionPool):
        self._pool = connection_pool

    def get_lock(self) -> asyncio.Lock:
        raise NotImplementedError()

    async def initialize(self):
        async with self._pool.transaction() as cur:
            await cur.execute("""CREATE TABLE IF NOT EXISTS friendship(
                user1_id INTEGER,
                user2_id INTEGER,
                PRIMARY KEY (user1_id, user2_id),
                FOREIGN KEY (user1_id) REFERENCES user(user_id) ON DELETE CASCADE,
                FOREIGN KEY (user2_id) REFERENCES user(user_id) ON DELETE CASCADE)""")

    async def check_friendship(self, user1_id: int, user2_id: int) -> bool:
        user1_id, user2_id = min(user1_id, user2_id), max(user1_id, user2_id)
        async with self._pool.transaction() as cur:
            await cur.execute("SELECT 1 FROM friendship WHERE user1_id = ? AND user2_id = ?",
                              (user1_id, user2_id))
            row = await cur.fetchone()
            return row is not None

    async def get_all_friends(self, user_id: int) -> Sequence[int]:
        result = list()

        async with self._pool.transaction() as cur:
            await cur.execute("SELECT user2_id FROM friendship WHERE user1_id = ?", (user_id,))
            rows = await cur.fetchall()
            result.extend(rows)

            await cur.execute("SELECT user1_id FROM friendship WHERE user2_id = ?", (user_id,))
            rows = await cur.fetchall()
            result.extend(rows)

        return [row[0] for row in result]

    async def add_friendship(self, user1_id: int, user2_id: int) -> None:
        user1_id, user2_id = min(user1_id, user2_id), max(user1_id, user2_id)
        async with self._pool.transaction(TransactionType.Immediate) as cur:
            await cur.execute(
                "INSERT OR IGNORE INTO friendship(user1_id, user2_id) VALUES (?, ?)", (user1_id, user2_id))

    async def try_remove_friendship(self, user1_id: int, user2_id: int) -> bool:
        user1_id, user2_id = min(user1_id, user2_id), max(user1_id, user2_id)
        async with self._pool.transaction(TransactionType.Immediate) as cur:
            await cur.execute("SELECT 1 FROM friendship WHERE user1_id = ? AND user2_id = ?", (user1_id, user2_id))
            row = await cur.fetchone()
            if row is None:
                return False
            await cur.execute(
                "DELETE FROM friendship WHERE user1_id = ? AND user2_id = ?", (user1_id, user2_id))
