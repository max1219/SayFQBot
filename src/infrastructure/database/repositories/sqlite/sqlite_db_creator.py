import aiosqlite
import asyncio

from typing import Tuple

from . import SqliteFqRepo, SqliteUserRepo, SqliteFriendshipRequestRepo, SqliteFriendshipRepo

async def ensure_created_and_get_repos(db_file_path: str) -> (
        Tuple)[SqliteFqRepo, SqliteUserRepo, SqliteFriendshipRepo, SqliteFriendshipRequestRepo]:
    connection: aiosqlite.Connection = await aiosqlite.connect(db_file_path)

    await connection.execute("PRAGMA foreign_keys = ON")

    # Если 2 репозитория будут использовать одну блокировку, нужно передавать один Lock.
    # Однако нужно будет быть осторожным, чтобы нигде случайно 2 раза этот самый один лок не попытаться занять

    fq_repo = SqliteFqRepo(connection, asyncio.Lock())
    user_repo = SqliteUserRepo(connection, asyncio.Lock())
    friendship_repo = SqliteFriendshipRepo(connection, asyncio.Lock())
    friendship_request_repo = SqliteFriendshipRequestRepo(connection, asyncio.Lock())

    await user_repo.initialize()
    await fq_repo.initialize()
    await friendship_repo.initialize()
    await friendship_request_repo.initialize()


    return fq_repo, user_repo, friendship_repo, friendship_request_repo