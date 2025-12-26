import asyncio

import aiosqlite

from typing import Sequence

from src.domain.repositories import IFriendshipRepo


class SqliteFriendshipRepo(IFriendshipRepo):
    def __init__(self, connection: aiosqlite.Connection, lock: asyncio.Lock):
        self._connection = connection
        self._lock = lock

    def get_lock(self) -> asyncio.Lock:
        return self._lock

    async def initialize(self):
        await self._connection.execute("""CREATE TABLE IF NOT EXISTS friendship(
            user1_id INTEGER,
            user2_id INTEGER,
            PRIMARY KEY (user1_id, user2_id),
            FOREIGN KEY (user1_id) REFERENCES user(user_id) ON DELETE CASCADE,
            FOREIGN KEY (user2_id) REFERENCES user(user_id) ON DELETE CASCADE)""")
        await self._connection.commit()

    async def check_friendship(self, user1_id: int, user2_id: int) -> bool:
        user1_id, user2_id = min(user1_id, user2_id), max(user1_id, user2_id)
        async with self._connection.cursor() as cur:
            await cur.execute("SELECT 1 FROM friendship WHERE user1_id = ? AND user2_id = ?",
                              (user1_id, user2_id))
            row = await cur.fetchone()
            return row is not None

    async def get_all_friends(self, user_id: int) -> Sequence[int]:
        async with self._connection.cursor() as cur:
            result = list()

            await cur.execute("SELECT user2_id FROM friendship WHERE user1_id = ?", (user_id,))
            rows = await cur.fetchall()
            result.extend(rows)

            await cur.execute("SELECT user1_id FROM friendship WHERE user2_id = ?", (user_id,))
            rows = await cur.fetchall()
            result.extend(rows)

        return [row[0] for row in result]

    async def add_friendship(self, user1_id: int, user2_id: int) -> None:
        user1_id, user2_id = min(user1_id, user2_id), max(user1_id, user2_id)
        async with self._connection.cursor() as cur:
            await cur.execute(
                "INSERT OR IGNORE INTO friendship(user1_id, user2_id) VALUES (?, ?)", (user1_id, user2_id))
            await self._connection.commit()

    async def remove_friendship(self, user1_id: int, user2_id: int) -> None:
        user1_id, user2_id = min(user1_id, user2_id), max(user1_id, user2_id)
        async with self._connection.cursor() as cur:
            await cur.execute(
                "DELETE FROM friendship WHERE user1_id = ? AND user2_id = ?", (user1_id, user2_id))
            await self._connection.commit()
