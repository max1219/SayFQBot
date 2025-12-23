import asyncio

import aiosqlite

from typing import Optional

from src.domain.entities import User
from src.domain.repositories import IUserRepo


class SqliteUserRepo(IUserRepo):
    def __init__(self, connection: aiosqlite.Connection, lock: asyncio.Lock):
        self._connection = connection
        self._lock = lock

    def get_lock(self) -> asyncio.Lock:
        return self._lock

    async def initialize(self):
        await self._connection.execute("""CREATE TABLE IF NOT EXISTS user(
        user_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL UNIQUE)""")
        await self._connection.commit()

    async def is_exists(self, user_id: int) -> bool:
        async with self._connection.cursor() as cur:
            await cur.execute("SELECT 1 FROM user WHERE user_id = ?", (user_id,))
            row = await cur.fetchone()
            return row is not None

    async def get_by_name(self, name: str) -> Optional[User]:
        async with self._connection.cursor() as cur:
            await cur.execute("SELECT * FROM user WHERE name = ?", (name,))
            row = await cur.fetchone()
            if row is None:
                return None
            return User(row[0], row[1])

    async def get_by_id(self, user_id: int) -> Optional[User]:
        async with self._connection.cursor() as cur:
            await cur.execute("SELECT * FROM user WHERE user_id = ?", (user_id,))
            row = await cur.fetchone()
            if row is None:
                return None
            return User(row[0], row[1])

    async def add_user(self, user: User) -> None:
        async with self._connection.cursor() as cur:
            await cur.execute("INSERT OR IGNORE INTO user(user_id, name) VALUES(?, ?)",
                                    (user.user_id, user.name))
            await self._connection.commit()
