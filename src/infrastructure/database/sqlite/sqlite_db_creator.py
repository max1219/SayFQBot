from typing import Tuple

from . import SqliteFqRepo, SqliteUserRepo, SqliteFriendshipRequestRepo, SqliteFriendshipRepo
from .connection_pool import ConnectionPool


async def ensure_created_and_get_repos(db_file_path: str) -> (
        Tuple)[SqliteFqRepo, SqliteUserRepo, SqliteFriendshipRepo, SqliteFriendshipRequestRepo]:
    pool: ConnectionPool = ConnectionPool(db_file_path)

    user_repo = SqliteUserRepo(pool)
    fq_repo = SqliteFqRepo(pool)
    friendship_repo = SqliteFriendshipRepo(pool)
    friendship_request_repo = SqliteFriendshipRequestRepo(pool)

    await user_repo.initialize()
    await fq_repo.initialize()
    await friendship_repo.initialize()
    await friendship_request_repo.initialize()

    return fq_repo, user_repo, friendship_repo, friendship_request_repo
