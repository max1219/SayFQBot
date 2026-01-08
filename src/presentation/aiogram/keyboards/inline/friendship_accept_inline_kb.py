from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.presentation.aiogram.keyboards.callbacks import FriendshipAcceptCallback


def create_friendship_accept_kb(requested_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text='Принять',
                             callback_data=FriendshipAcceptCallback(user_id=requested_id).pack()),
        InlineKeyboardButton(text='Не, нахуй',
                             callback_data='friend_deny')]])
