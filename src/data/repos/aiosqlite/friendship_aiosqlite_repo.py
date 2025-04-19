from typing import Iterable

from aiosqlite import Cursor, Row

from .. import IFriendshipRepo
from ...entities import User, Friendship


class FriendshipAioSQLiteRepo(IFriendshipRepo):
    def __init__(self, cursor: Cursor):
        self._cursor = cursor

    async def create_table(self) -> None:
        await self._cursor.execute('''
            CREATE TABLE IF NOT EXISTS friendship (
                user1_id INT NOT NULL,
                user2_id INT NOT NULL,
                PRIMARY KEY (user1_id, user2_id),
                FOREIGN KEY (user1_id) REFERENCES users(id) ON DELETE RESTRICT ON UPDATE RESTRICT,
                FOREIGN KEY (user2_id) REFERENCES users(id) ON DELETE RESTRICT ON UPDATE RESTRICT)
            ''')

    async def is_friends(self, friendship: Friendship) -> bool:
        await self._cursor.execute("SELECT EXISTS(SELECT 1 FROM friendship "
                                   "    WHERE user1_id = ? AND user2_id = ?"
                                   "       OR user2_id = ? AND user1_id = ?)",
                                   (friendship.user1_id, friendship.user2_id,
                                    friendship.user1_id, friendship.user2_id))
        row: Row = await self._cursor.fetchone()
        return row[0] == 1

    async def get_all(self, user: User) -> Iterable[Friendship]:
        await self._cursor.execute("SELECT * FROM friendship WHERE user1_id = ? OR user2_id = ?",
                                   (user.id, user.id))
        rows: Iterable[Row] = await self._cursor.fetchall()
        return map(lambda row: Friendship(row['user1_id'], row['user2_id']), rows)

    async def add(self, friendship: Friendship) -> None:
        await self._cursor.execute("INSERT INTO friendship VALUES (?, ?)",
                                   (friendship.user1_id, friendship.user2_id))

    async def remove(self, friendship: Friendship) -> None:
        await self._cursor.execute("DELETE FROM friendship WHERE user1_id = ? AND user2_id = ?",
                                   (friendship.user1_id, friendship.user2_id))
