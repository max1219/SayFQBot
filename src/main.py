import logging

import asyncio

from aiogram import Bot, Dispatcher

from src.presentation.aiogram.middlewares.ensure_registered_middleware import EnsureRegisteredMiddleware
from src.presentation.aiogram.handlers import temp_handler, debug_handlers, okay_handler, send_fq_handlers

from src.presentation.aiogram.message_senders import *
from src.presentation.console_demo.message_senders import *
from src.debug_helpers.proxy_message_senders import *
from src.presentation.aiogram.services import SendMenuService, IsAdminService

from src.domain.services.implementations import FqService, FriendshipService, SingleFqLimitsService, UserService, \
    ConstantFqLimitProvider
from src.infrastructure.database.repositories.sqlite import *

from src.config import Config, load_config

async def create_and_add_services(bot: Bot, dp: Dispatcher, config: Config):
    fq_repo: SqliteFqRepo
    user_repo: SqliteUserRepo
    friendship_repo: SqliteFriendshipRepo
    friendship_request_repo: SqliteFriendshipRequestRepo

    fq_repo, user_repo, friendship_repo, friendship_request_repo = (
        await ensure_created_and_get_repos(config.database.path))

    friendship_message_sender = AiogramFriendshipMessageSender(bot)
    fake_friendship_message_sender = ConsoleFriendshipMessageSender()
    fq_message_sender = AiogramFqMessageSender(bot)
    fake_fq_message_sender = ConsoleFqMessageSender()

    if config.bot.debug_features:
        friendship_message_sender = ProxyFriendshipMessageSender(
            friendship_message_sender, fake_friendship_message_sender, lambda i: i > 1000)
        fq_message_sender = ProxyFqMessageSender(
            fq_message_sender, fake_fq_message_sender, lambda i: i > 1000)

    fq_limits_provider = ConstantFqLimitProvider(2)
    fq_limits_service = SingleFqLimitsService(fq_limits_provider, fq_repo)

    fq_service = FqService(fq_message_sender, friendship_repo, user_repo, fq_limits_service, fq_repo)
    friendship_service = FriendshipService(friendship_repo, friendship_request_repo, user_repo,
                                           friendship_message_sender)
    user_service = UserService(user_repo)

    send_menu_service = SendMenuService(user_service, friendship_service, fq_limits_service, 5, bot)
    is_admin_service = IsAdminService(config.bot.admin_ids)

    dp['user_service'] = user_service
    dp['friendship_service'] = friendship_service
    dp['fq_service'] = fq_service
    dp['fq_limits_service'] = fq_limits_service
    dp['send_menu_service'] = send_menu_service
    dp['is_admin_service'] = is_admin_service


async def main() -> None:
    config: Config = load_config('../.env')
    logging.basicConfig(level=config.logging.level)
    logging.getLogger('aiosqlite').setLevel(logging.WARNING)
    bot = Bot(token=config.bot.token)
    await bot.delete_webhook(drop_pending_updates=True)
    dp = Dispatcher()

    await create_and_add_services(bot, dp, config)

    dp.update.outer_middleware(EnsureRegisteredMiddleware())

    if config.bot.debug_features:
        dp.include_router(debug_handlers.router)
    dp.include_router(okay_handler.router)
    dp.include_router(send_fq_handlers.router)
    dp.include_router(temp_handler.router)

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
