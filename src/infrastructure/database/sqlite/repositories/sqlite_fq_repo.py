import asyncio

from src.domain.repositories import IFqRepo
from src.domain.repositories.operation_results import AddFqStatus
from src.infrastructure.database.sqlite.connection_pool import ConnectionPool
from src.infrastructure.database.sqlite.transaction_type import TransactionType


class SqliteFqRepo(IFqRepo):
    def __init__(self, connection_pool: ConnectionPool):
        self._pool = connection_pool

    def get_lock(self) -> asyncio.Lock:
        raise NotImplementedError()

    async def initialize(self):
        async with self._pool.transaction() as cur:
            await cur.execute("""CREATE TABLE IF NOT EXISTS fq(
            user_from_id INTEGER NOT NULL,
            user_to_id INTEGER NOT NULL,
            FOREIGN KEY (user_from_id) REFERENCES user (user_id) ON DELETE CASCADE,
            FOREIGN KEY (user_to_id) REFERENCES user (user_id) ON DELETE CASCADE)""")

    async def try_add_fq(self, id_from: int, id_to: int, limit_total: int, limit_to:int) -> AddFqStatus:
        async with self._pool.transaction(TransactionType.Immediate) as cur:
            await cur.execute("SELECT COUNT(1) FROM fq WHERE user_from_id = ?", (id_from,))
            row = await cur.fetchone()
            count_total = row[0]
            await cur.execute("SELECT COUNT(1) FROM fq WHERE user_from_id = ? AND user_to_id = ?", (id_from, id_to))
            row = await cur.fetchone()
            count_to = row[0]

            result: AddFqStatus = AddFqStatus(0)
            if count_total >= limit_total:
                result |= AddFqStatus.TotalLimitExceeded
            if count_to >= limit_to:
                result |= AddFqStatus.ToThisFriendLimitExceeded

            if result == AddFqStatus(0):
                await cur.execute("INSERT INTO fq (user_from_id, user_to_id) VALUES (?, ?)", (id_from, id_to))
            return result

    async def remove_fq(self, id_from: int, id_to: int) -> None:
        async with self._pool.transaction(TransactionType.Immediate) as cur:
            await cur.execute("DELETE FROM fq WHERE user_from_id = ? AND user_to_id = ?", (id_from, id_to))

    async def clear(self) -> None:
        async with self._pool.transaction(TransactionType.Immediate) as cur:
            # noinspection SqlWithoutWhere
            await cur.execute("DELETE FROM fq")

    async def get_total_sent_count(self, id_from: int) -> int:
        async with self._pool.transaction() as cur:
            await cur.execute("SELECT COUNT(1) FROM fq WHERE user_from_id = ?", (id_from,))
            row = await cur.fetchone()
            return row[0]

    async def get_to_this_friend_sent_count(self, id_from: int, id_to: int) -> int:
        async with self._pool.transaction() as cur:
            await cur.execute("SELECT COUNT(1) FROM fq WHERE user_from_id = ? AND user_to_id = ?", (id_from, id_to))
            row = await cur.fetchone()
            return row[0]



