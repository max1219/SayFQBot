from typing import Optional

from aiosqlite import Cursor, Row

from .. import IUserRepo
from ...entities import User


class UserAioSQLiteRepo(IUserRepo):
    def __init__(self, cursor: Cursor):
        self._cursor = cursor

    async def create_table(self) -> None:
        await self._cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INT PRIMARY KEY,
                username TEXT NOT NULL,
                n_friends INT NOT NULL)
            ''')

    async def get_by_id(self, user_id: int) -> Optional[User]:
        await self._cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row: Row = await self._cursor.fetchone()
        if row is None:
            return None
        return User(id=row['id'], username=row['username'], n_friends=row['n_friends'])

    async def get_by_username(self, username: str) -> Optional[User]:
        await self._cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        row: Row = await self._cursor.fetchone()
        if row is None:
            return None
        return User(id=row['id'], username=row['username'], n_friends=row['n_friends'])

    async def add(self, user: User) -> None:
        await self._cursor.execute("INSERT INTO users VALUES (?, ?, ?)",
                                   (user.id, user.username, user.n_friends))

    async def remove(self, user: User) -> None:
        await self._cursor.execute("DELETE FROM users WHERE id = ?", (user.id,))

    async def edit(self, user: User) -> None:
        await self._cursor.execute("UPDATE users SET username = ?, n_friends = ? WHERE id = ?",
                                   (user.username, user.n_friends, user.id))
