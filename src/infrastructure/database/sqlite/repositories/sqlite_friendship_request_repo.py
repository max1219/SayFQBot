import asyncio
from typing import Sequence

from src.domain.repositories import IFriendshipRequestRepo
from src.infrastructure.database.sqlite.connection_pool import ConnectionPool
from src.infrastructure.database.sqlite.transaction_type import TransactionType


class SqliteFriendshipRequestRepo(IFriendshipRequestRepo):
    def __init__(self, connection_pool: ConnectionPool):
        self._pool = connection_pool

    def get_lock(self) -> asyncio.Lock:
        raise NotImplementedError()

    async def initialize(self):
        async with self._pool.transaction() as cur:
            await cur.execute("""CREATE TABLE IF NOT EXISTS friendship_request(
            user_from_id INTEGER,
            user_to_id INTEGER,
            PRIMARY KEY (user_from_id, user_to_id),
            FOREIGN KEY (user_from_id) REFERENCES user (user_id) ON DELETE CASCADE,
            FOREIGN KEY (user_to_id) REFERENCES user (user_id) ON DELETE CASCADE)""")

    async def try_add_request(self, user1_id: int, user2_id: int) -> bool:
        async with self._pool.transaction(TransactionType.Immediate) as cur:
            await cur.execute("SELECT 1 FROM friendship_request WHERE user_from_id = ? AND user_to_id = ?",
                              (user1_id, user2_id))
            row = await cur.fetchone()
            if row is not None:
                return False
            await cur.execute("INSERT OR IGNORE INTO friendship_request VALUES (?, ?)", (user1_id, user2_id))
            return True

    async def try_remove_request(self, user1_id: int, user2_id: int, ignore_order: bool) -> bool:
        async with self._pool.transaction(TransactionType.Immediate) as cur:
            await cur.execute("""
            SELECT 1 FROM friendship_request 
            WHERE user_from_id = ? AND user_to_id = ?
            OR ? AND user_to_id = ? AND user_from_id = ?""",
                              (user1_id, user2_id, ignore_order, user1_id, user2_id))
            row = await cur.fetchone()
            if row is None:
                return False

            await cur.execute("""
            DELETE FROM friendship_request 
            WHERE user_from_id = ? AND user_to_id = ?
            OR ? AND user_to_id = ? AND user_from_id = ?""",
                              (user1_id, user2_id, ignore_order, user1_id, user2_id))

            return True

    async def is_exists(self, user1_id: int, user2_id: int, ignore_order: bool) -> bool:
        async with self._pool.transaction() as cur:
            await cur.execute("""
            SELECT 1 FROM friendship_request 
            WHERE user_from_id = ? AND user_to_id = ?
            OR ? AND user_to_id = ? AND user_from_id = ?""",
                              (user1_id, user2_id, ignore_order, user1_id, user2_id))
            row = await cur.fetchone()
            return row is not None

    async def get_incoming_requests(self, user_to_id: int) -> Sequence[int]:
        async with self._pool.transaction() as cur:
            await cur.execute("SELECT user_from_id FROM friendship_request WHERE user_to_id = ?", (user_to_id,))
            rows = await cur.fetchall()
            return [row[0] for row in rows]
