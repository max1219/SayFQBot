from typing import Iterable, Optional

from aiosqlite import Cursor, Row

from .. import IFriendshipRequestRepo
from ...entities import User, Friendship, FriendshipRequest


class FriendshipRequestAioSQLiteRepo(IFriendshipRequestRepo):
    def __init__(self, cursor: Cursor):
        self._cursor = cursor

    async def create_table(self) -> None:
        await self._cursor.execute('''
            CREATE TABLE IF NOT EXISTS friendship_request (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_from_id INT NOT NULL,
                user_to_id INT NOT NULL,
                is_expired BOOLEAN NOT NULL,
                FOREIGN KEY (user_from_id) REFERENCES users (id) ON DELETE RESTRICT ON UPDATE RESTRICT,
                FOREIGN KEY(user_to_id) REFERENCES users (id) ON DELETE RESTRICT ON UPDATE RESTRICT)
            ''')

    async def get_unordered(self, friendship: Friendship) -> Optional[FriendshipRequest]:
        await self._cursor.execute("SELECT id, user_from_id, user_to_id FROM friendship_request"
                                   " WHERE user_from_id = ? AND user_to_id = ?"
                                   "    OR user_to_id = ? AND user_from_id = ?",
                                   (friendship.user1_id, friendship.user2_id,
                                    friendship.user1_id, friendship.user2_id))
        row: Row = await self._cursor.fetchone()
        if row is None:
            return None
        return FriendshipRequest(id=row['id'], user_from_id=row['user_from_id'], user_to_id=row['user_to_id'])

    async def get_all_incoming(self, user: User) -> Iterable[FriendshipRequest]:
        await self._cursor.execute("SELECT id, user_from_id, user_to_id FROM friendship_request"
                                   " WHERE user_to_id = ?")
        rows: Iterable[Row] = await self._cursor.fetchall()
        return map(
            lambda row: FriendshipRequest(id=row['id'], user_from_id=row['user_from_id'], user_to_id=row['user_to_id']),
            rows)

    async def add(self, friendship_request: FriendshipRequest) -> int:
        await self._cursor.execute("INSERT INTO friendship_request "
                             "(user_from_id, user_to_id, is_expired) VALUES (?, ?, FALSE)",
                             (friendship_request.user_from_id, friendship_request.user_to_id))
        return self._cursor.lastrowid

    async def remove(self, friendship_request: FriendshipRequest) -> None:
        await self._cursor.execute("DELETE FROM friendship_request WHERE id = ?",
                                   (friendship_request.id,))

    async def cleanup(self) -> int:
        await self._cursor.execute("DELETE FROM friendship_request WHERE is_expired = TRUE")
        n_deleted: int = self._cursor.rowcount
        await self._cursor.execute("UPDATE friendship_request SET is_expired = TRUE WHERE TRUE")
        return n_deleted