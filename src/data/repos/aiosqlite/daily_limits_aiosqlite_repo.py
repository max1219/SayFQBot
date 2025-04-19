from typing import Iterable, Optional

from aiosqlite import Cursor, Row

from .. import IDayLimitsRepo
from ...entities import User, DailyLimits


class DailyLimitsAioSQLiteRepo(IDayLimitsRepo):
    def __init__(self, cursor: Cursor):
        self._cursor = cursor

    async def create_table(self) -> None:
        await self._cursor.execute('''
            CREATE TABLE IF NOT EXISTS daily_limits (
                user_id INTEGER PRIMARY KEY,
                friendship_requests INT NOT NULL,
                fqs INT NOT NULL,
                fqs_all INT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE RESTRICT ON UPDATE RESTRICT)
            ''')

    async def get_by_user(self, user: User) -> Optional[DailyLimits]:
        await self._cursor.execute("SELECT * FROM daily_limits WHERE user_id = ?", (user.id,))
        row: Row = await self._cursor.fetchone()
        if row is None:
            return None
        return DailyLimits(user_id=row['user_id'], friendship_requests=row['friendship_requests'],
                           fqs=row['fqs'], fqs_all=row['fqs_all'])

    async def add(self, daily_limits: DailyLimits) -> None:
        await self._cursor.execute("INSERT INTO daily_limits VALUES (?,?,?,?)",
                                   (daily_limits.user_id, daily_limits.friendship_requests,
                                    daily_limits.fqs, daily_limits.fqs_all))

    async def remove(self, daily_limits: DailyLimits) -> None:
        await self._cursor.execute("DELETE FROM daily_limits WHERE user_id = ?", (daily_limits.user_id,))

    async def edit(self, daily_limits: DailyLimits) -> None:
        await self._cursor.execute(
            "UPDATE daily_limits SET friendship_requests = ?, fqs = ?, fqs_all = ? WHERE user_id = ?",
            (daily_limits.friendship_requests, daily_limits.fqs, daily_limits.fqs_all, daily_limits.user_id))
