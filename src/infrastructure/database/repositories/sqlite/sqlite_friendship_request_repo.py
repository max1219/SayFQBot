import asyncio

import aiosqlite

from src.domain.repositories import IFriendshipRequestRepo


class SqliteFriendshipRequestRepo(IFriendshipRequestRepo):
    def __init__(self, connection: aiosqlite.Connection, lock: asyncio.Lock):
        self._connection = connection
        self._lock = lock

    def get_lock(self) -> asyncio.Lock:
        return self._lock

    async def initialize(self):
        await self._connection.execute("""CREATE TABLE IF NOT EXISTS friendship_request(
        user_from_id INTEGER,
        user_to_id INTEGER,
        PRIMARY KEY (user_from_id, user_to_id),
        FOREIGN KEY (user_from_id) REFERENCES user (user_id) ON DELETE CASCADE,
        FOREIGN KEY (user_to_id) REFERENCES user (user_id) ON DELETE CASCADE)""")
        await self._connection.commit()

    async def add_request(self, user1_id: int, user2_id: int) -> None:
        async with self._connection.cursor() as cur:
            await cur.execute("INSERT OR IGNORE INTO friendship_request VALUES (?, ?)", (user1_id, user2_id))
            await self._connection.commit()

    async def remove_request(self, user1_id: int, user2_id: int, ignore_order: bool) -> None:
        async with self._connection.cursor() as cur:
            await cur.execute("DELETE FROM friendship_request WHERE user_from_id = ? AND user_to_id = ?",
                (user1_id, user2_id))

            if ignore_order:
                await cur.execute(
                    "DELETE FROM friendship_request WHERE user_from_id = ? AND user_to_id = ?",
                    (user2_id, user1_id))

            await self._connection.commit()

    async def is_exists(self, user1_id: int, user2_id: int, ignore_order: bool) -> bool:
        async with self._connection.cursor() as cur:
            await cur.execute("SELECT 1 FROM friendship_request WHERE user_from_id = ? AND user_to_id = ?",
                (user1_id, user2_id))
            row = await cur.fetchone()

            if row is not None:
                return True

            if not ignore_order:
                return False

            await cur.execute("SELECT 1 FROM friendship_request WHERE user_from_id = ? AND user_to_id = ?",
                (user2_id, user1_id))
            row = await cur.fetchone()
            return row is not None
