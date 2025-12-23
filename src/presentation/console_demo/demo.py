from src.domain.services.implementations.friendship_service import FriendshipService
from src.infrastructure.database.repositories.sqlite import *
from src.domain.services.implementations.fq_service import FqService
from src.domain.services.implementations.single_fq_limits_service import SingleFqLimitsService
from src.domain.services.implementations.constant_fq_limit_provider import ConstantFqLimitProvider
from src.domain.entities.user import User

from src.presentation.console_demo.message_senders import ConsoleFriendshipMessageSender, ConsoleFqMessageSender


async def start_demo():
    fq_repo: SqliteFqRepo
    user_repo: SqliteUserRepo
    friendship_repo: SqliteFriendshipRepo
    friendship_request_repo: SqliteFriendshipRequestRepo

    fq_repo, user_repo, friendship_repo, friendship_request_repo = (
        await ensure_created_and_get_repos("infrastructure/database/db.sqlite"))

    friendship_message_sender = ConsoleFriendshipMessageSender()
    fq_message_sender = ConsoleFqMessageSender()
    friendship_service = FriendshipService(friendship_repo, friendship_request_repo, user_repo,
                                           friendship_message_sender)

    fq_limits_provider = ConstantFqLimitProvider(2)
    fq_limits_service = SingleFqLimitsService(fq_limits_provider, fq_repo)
    fq_service = FqService(fq_message_sender, friendship_repo, user_repo, fq_limits_service, fq_repo)
    await user_repo.add_user(User(0, "Zero"))
    await user_repo.add_user(User(1, "One"))
    await user_repo.add_user(User(2, "Two"))
    await user_repo.add_user(User(3, "Three"))

    print("Zero friends:", await friendship_service.get_all_friends(0))
    print("Wrong accept friendship:", await friendship_service.accept_friendship(0, 1))
    print("Send request to unregistered:", await friendship_service.request_friendship(0, "None"))
    print("Send request normal:", await friendship_service.request_friendship(0, "One"))
    await friendship_service.request_friendship(0, "Two")
    await friendship_service.request_friendship(0, "Three")
    print("Accept friendship:", await friendship_service.accept_friendship(1, 0))
    await friendship_service.accept_friendship(2, 0)
    print("Zero friends:", await friendship_service.get_all_friends(0))

    print("\n---FQ---")
    print("Success fq:", await fq_service.send_fq(0, 1))
    print("Repeating fq:", await fq_service.send_fq(0, 1))
    print("Fq to unregistered:", await fq_service.send_fq(0, 10))
    print("Fq to not friend:", await fq_service.send_fq(0, 3))
    print("Fq success second and last:", await fq_service.send_fq(0, 2))
    print("Fq over limit:", await fq_service.send_fq(0, 1))
    print("A new day")
    await fq_repo.clear()
    print("Success fq:", await fq_service.send_fq(0, 1))
