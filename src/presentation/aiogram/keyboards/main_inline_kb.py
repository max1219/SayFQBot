from typing import Iterable, Optional

from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton, InlineKeyboardMarkup
from src.presentation.aiogram.keyboards.types import FriendEntry, PaginationData
from src.presentation.aiogram.keyboards.callbacks import FriendSelectCallback, FriendFqCallback, PageSelectCallback


def create_main_kb(
        friends: Iterable[FriendEntry],
        pagination_data: Optional[PaginationData]
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    page: int = 1
    if pagination_data:
        page = pagination_data.current_page
    for friend in friends:
        builder.row(
            InlineKeyboardButton(text=friend.name,
                                 callback_data=FriendSelectCallback(user_id=friend.user_id, page=page).pack()),
            InlineKeyboardButton(text=('Уже послан' if friend.is_already_sent else 'Послать'),
                                 callback_data=FriendFqCallback(user_id=friend.user_id).pack())
        )

    if pagination_data:
        buttons = []
        if pagination_data.current_page > 1:
            buttons.append(InlineKeyboardButton(text='<', callback_data=PageSelectCallback(page=page - 1).pack()))

        buttons.append(InlineKeyboardButton(
            text=f'{pagination_data.current_page}/{pagination_data.total_pages}',
            callback_data='page_nothing'))

        if pagination_data.current_page < pagination_data.total_pages:
            buttons.append(InlineKeyboardButton(text='>', callback_data=PageSelectCallback(page=page + 1).pack()))

        builder.row(
            *buttons
        )

    builder.row(InlineKeyboardButton(text='Добавить друга', callback_data='friend_search'))

    return builder.as_markup()
