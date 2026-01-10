from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.domain.services.presentation import LexiconBase
from src.presentation.aiogram.keyboards.callbacks import FriendConfirmDeleteCallback


def create_friend_delete_confirmation_kb(friend_id: int, lexicon: LexiconBase) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text=lexicon.get('kb_friend_delete_confirm'),
                             callback_data=FriendConfirmDeleteCallback(user_id=friend_id).pack()),
        InlineKeyboardButton(text=lexicon.get('kb_friend_remove_not_confirm'),
                             callback_data='close_it')]])
