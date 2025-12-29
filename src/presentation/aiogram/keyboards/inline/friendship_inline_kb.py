from typing import Sequence

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.presentation.aiogram.keyboards.callbacks import FriendshipAcceptCallback


def create_friendship_accept_kb(requested_ids: int | Sequence[int]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    if isinstance(requested_ids, int):
        requested_ids = [requested_ids]

    for requested_id in requested_ids:
        builder.row(
            InlineKeyboardButton(text='Принять',
                                 callback_data=FriendshipAcceptCallback(user_id=requested_id).pack()),
            InlineKeyboardButton(text='Не, нахуй',
                                 callback_data='friend_deny'),
        )

    return builder.as_markup()
