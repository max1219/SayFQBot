import asyncio

from contextlib import asynccontextmanager

from typing import AsyncIterator

import aiosqlite
from aiosqlite import Cursor, Connection

from src.infrastructure.database.sqlite.transaction_type import TransactionType


class ConnectionPool:
    def __init__(self, path: str):
        self._queue = asyncio.Queue()
        self._path = path

    @asynccontextmanager
    async def transaction(self, transaction_type: TransactionType = TransactionType.Deferred) -> AsyncIterator[Cursor]:
        conn: Connection = await self._get_connection()
        cursor: Cursor = await conn.cursor()

        if transaction_type == TransactionType.Deferred:
            await cursor.execute("BEGIN")
        elif transaction_type == TransactionType.Immediate:
            await cursor.execute("BEGIN IMMEDIATE")
        elif transaction_type == TransactionType.Exclusive:
            await cursor.execute("BEGIN EXCLUSIVE")

        try:
            yield cursor
            await conn.commit()
        except:
            await conn.rollback()
            raise
        finally:
            await cursor.close()
            await self._release_connection(conn)
            pass

    async def _get_connection(self) -> Connection:
        if self._queue.empty():
            conn = await aiosqlite.connect(self._path)
            await conn.execute("PRAGMA foreign_keys = ON")
            return conn
        else:
            return await self._queue.get()

    async def _release_connection(self, connection: Connection) -> None:
        await self._queue.put(connection)
