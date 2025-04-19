from typing import Tuple

import aiosqlite

from . import UserAioSQLiteRepo, FriendshipAioSQLiteRepo, FriendshipRequestAioSQLiteRepo, DailyLimitsAioSQLiteRepo

from .. import IDatabase


class DatabaseAioSQLite(IDatabase):
    def __init__(self, db_path: str) -> None:
        self._db_path = db_path

        self._connection = None
        self._cursor = None

        self._user_repo = None
        self._friendship_repo = None
        self._friendship_request_repo = None
        self._daily_limits_repo = None

    async def init(self) -> Tuple[
        UserAioSQLiteRepo, FriendshipAioSQLiteRepo, FriendshipRequestAioSQLiteRepo, DailyLimitsAioSQLiteRepo]:
        self._connection = await aiosqlite.connect(self._db_path, autocommit=True)
        self._cursor = await self._connection.cursor()
        self._user_repo = UserAioSQLiteRepo(self._cursor)
        self._friendship_repo = FriendshipAioSQLiteRepo(self._cursor)
        self._friendship_request_repo = FriendshipRequestAioSQLiteRepo(self._cursor)
        self._daily_limits_repo = DailyLimitsAioSQLiteRepo(self._cursor)

        await self._user_repo.create_table()
        await self._friendship_repo.create_table()
        await self._friendship_request_repo.create_table()
        await self._daily_limits_repo.create_table()

        return self._user_repo, self._friendship_repo, self._friendship_request_repo, self._daily_limits_repo
