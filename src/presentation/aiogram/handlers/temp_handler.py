import logging


from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from src.domain.dto.requests.user import AddUserRequest
from src.domain.services import IUserService, IFriendshipService
from src.presentation.aiogram.services import SendMenuService
from src.presentation.aiogram.keyboards.callbacks import PageSelectCallback

router = Router()


@router.message()
async def handler(message: Message, send_menu_service: SendMenuService):
    await send_menu_service.send_menu(message.from_user.id, 1)

@router.callback_query(PageSelectCallback.filter())
async def handle_callback(
        callback: CallbackQuery, callback_data: PageSelectCallback, send_menu_service: SendMenuService):
    await send_menu_service.send_menu(callback.from_user.id, callback_data.page, callback)

@router.callback_query(F.data == 'friend_search')
async def friend_search(
        callback: CallbackQuery,
        user_service: IUserService,
        friendship_service: IFriendshipService,
        send_menu_service: SendMenuService):
    fake_user_ids = filter(lambda i: i < 1000, map(lambda user: user.user_id, await user_service.get_all_users()))
    max_user_id: int = max(fake_user_ids, default=0)
    num = max_user_id + 1
    await user_service.add_user(AddUserRequest(num, f"user-{num}"))
    await friendship_service.request_friendship(callback.from_user.id, f"user-{num}")
    await friendship_service.accept_friendship(num, callback.from_user.id)
    await send_menu_service.send_menu(callback.from_user.id, 1)
