import asyncio
import aiosqlite

from src.domain.repositories import IFqRepo

class SqliteFqRepo(IFqRepo):
    def __init__(self, connection: aiosqlite.Connection, lock: asyncio.Lock):
        self._connection = connection
        self._lock = lock

    def get_lock(self) -> asyncio.Lock:
        return self._lock

    async def initialize(self):
        await self._connection.execute("""CREATE TABLE IF NOT EXISTS fq(
        user_from_id INTEGER NOT NULL,
        user_to_id INTEGER NOT NULL,
        FOREIGN KEY (user_from_id) REFERENCES user (user_id) ON DELETE CASCADE,
        FOREIGN KEY (user_to_id) REFERENCES user (user_id) ON DELETE CASCADE)""")
        await self._connection.commit()

    async def add_fq(self, id_from: int, id_to: int) -> None:
        async with self._connection.cursor() as cur:
            await cur.execute("INSERT INTO fq (user_from_id, user_to_id) VALUES (?, ?)", (id_from, id_to))
            await self._connection.commit()

    async def clear(self) -> None:
        async with self._connection.cursor() as cur:
            # noinspection SqlWithoutWhere
            await cur.execute("DELETE FROM fq")
            await self._connection.commit()

    async def get_total_sent_count(self, id_from: int) -> int:
        async with self._connection.cursor() as cur:
            await cur.execute("SELECT COUNT(1) FROM fq WHERE user_from_id = ?", (id_from,))
            row = await cur.fetchone()
            return row[0]

    async def get_to_this_friend_sent_count(self, id_from: int, id_to: int) -> int:
        async with self._connection.cursor() as cur:
            await cur.execute("SELECT COUNT(1) FROM fq WHERE user_from_id = ? AND user_to_id = ?", (id_from, id_to))
            row = await cur.fetchone()
            return row[0]



