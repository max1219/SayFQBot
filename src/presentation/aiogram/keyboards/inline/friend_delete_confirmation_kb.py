from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.presentation.aiogram.keyboards.callbacks import FriendConfirmDeleteCallback


def create_friend_delete_confirmation_kb(friend_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text='Да, а че еще делать?',
                             callback_data=FriendConfirmDeleteCallback(user_id=friend_id).pack()),
        InlineKeyboardButton(text='Не, лучше завтра',
                             callback_data='close_it')]])
