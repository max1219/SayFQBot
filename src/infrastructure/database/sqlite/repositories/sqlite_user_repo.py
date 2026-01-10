import asyncio

from typing import Optional, Sequence

from src.domain.entities import User
from src.domain.repositories import IUserRepo
from src.infrastructure.database.sqlite.connection_pool import ConnectionPool
from src.infrastructure.database.sqlite.transaction_type import TransactionType


class SqliteUserRepo(IUserRepo):
    def __init__(self, connection_pool: ConnectionPool):
        self._pool = connection_pool

    def get_lock(self) -> asyncio.Lock:
        raise NotImplementedError()

    async def initialize(self):
        async with self._pool.transaction() as cur:
            await cur.execute("""CREATE TABLE IF NOT EXISTS user(
            user_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL UNIQUE)""")

    async def is_exists(self, user_id: int) -> bool:
        async with self._pool.transaction() as cur:
            await cur.execute("SELECT 1 FROM user WHERE user_id = ?", (user_id,))
            row = await cur.fetchone()
            return row is not None

    async def get_by_name(self, name: str) -> Optional[User]:
        async with self._pool.transaction() as cur:
            await cur.execute("SELECT * FROM user WHERE name = ?", (name,))
            row = await cur.fetchone()
            if row is None:
                return None
            return User(row[0], row[1])

    async def get_by_id(self, user_id: int) -> Optional[User]:
        async with self._pool.transaction() as cur:
            await cur.execute("SELECT * FROM user WHERE user_id = ?", (user_id,))
            row = await cur.fetchone()
            if row is None:
                return None
            return User(row[0], row[1])

    async def try_add_user(self, user: User) -> bool:
        async with self._pool.transaction(TransactionType.Immediate) as cur:
            await cur.execute("SELECT 1 FROM user WHERE user_id = ?", (user.user_id,))
            row = await cur.fetchone()
            if row is not None:
                return False
            await cur.execute("INSERT OR IGNORE INTO user(user_id, name) VALUES(?, ?)",
                              (user.user_id, user.name))
            return True

    async def get_all_users(self) -> Sequence[User]:
        async with self._pool.transaction() as cur:
            await cur.execute("SELECT * FROM user")
            rows = await cur.fetchall()
            return [User(row[0], row[1]) for row in rows]

    async def remove_user(self, user_id: int) -> None:
        async with self._pool.transaction(TransactionType.Immediate) as cur:
            await cur.execute("DELETE FROM user WHERE user_id = ?", (user_id,))
