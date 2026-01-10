from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.domain.services.presentation import LexiconBase
from src.presentation.aiogram.keyboards.callbacks import FriendDeleteCallback


def create_selected_friend_kb(friend_id: int, lexicon: LexiconBase) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text=lexicon.get('kb_friend_delete'),
                             callback_data=FriendDeleteCallback(user_id=friend_id).pack()),
        InlineKeyboardButton(text=lexicon.get('kb_friend_not_delete'),
                             callback_data='close_it')]])
