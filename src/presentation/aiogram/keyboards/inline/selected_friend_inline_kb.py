from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.presentation.aiogram.keyboards.callbacks import FriendDeleteCallback


def create_selected_friend_kb(friend_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text='Удалить нахуй',
                             callback_data=FriendDeleteCallback(user_id=friend_id).pack()),
        InlineKeyboardButton(text='Пока оставить',
                             callback_data='close_it')]])
