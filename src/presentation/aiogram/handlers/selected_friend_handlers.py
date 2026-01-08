from aiogram import Router
from aiogram.types import CallbackQuery

from src.domain.services.interfaces.i_friendship_service import IFriendshipService
from src.domain.services.interfaces.i_user_service import IUserService

from src.presentation.aiogram.keyboards.callbacks import FriendSelectCallback, FriendDeleteCallback, \
    FriendConfirmDeleteCallback
from src.presentation.aiogram.keyboards.inline import create_selected_friend_kb, create_friend_delete_confirmation_kb, \
    create_okay_kb
from src.presentation.aiogram.services import SendMenuService
router = Router()


@router.callback_query(FriendSelectCallback.filter())
async def cb_friend_select(callback: CallbackQuery, callback_data: FriendSelectCallback, user_service: IUserService):
    name = (await user_service.get_by_id(callback_data.user_id)).name
    text = f'Что будем делать с @{name}?'
    await callback.message.answer(text=text, reply_markup=create_selected_friend_kb(callback_data.user_id))
    await callback.answer()


@router.callback_query(FriendDeleteCallback.filter())
async def cb_friend_delete(callback: CallbackQuery, callback_data: FriendDeleteCallback):
    await callback.message.edit_text(
        text='Вы уверены?', reply_markup=create_friend_delete_confirmation_kb(callback_data.user_id))


@router.callback_query(FriendConfirmDeleteCallback.filter())
async def cb_confirm_delete(callback: CallbackQuery, callback_data: FriendConfirmDeleteCallback,
                            friendship_service: IFriendshipService, send_menu_service: SendMenuService):
    await friendship_service.remove_friendship(callback.from_user.id, callback_data.user_id)
    await send_menu_service.send_menu(callback.from_user.id, callback=callback)
    await callback.message.answer(text='Друг удален', reply_markup=create_okay_kb())
