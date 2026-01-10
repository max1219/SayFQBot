from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.domain.services.presentation import LexiconBase
from src.presentation.aiogram.keyboards.callbacks import FriendshipAcceptCallback


def create_friendship_accept_kb(requested_id: int, lexicon: LexiconBase) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text=lexicon.get('kb_friend_accept'),
                             callback_data=FriendshipAcceptCallback(user_id=requested_id).pack()),
        InlineKeyboardButton(text=lexicon.get('kb_friend_dont_accept'),
                             callback_data='friend_deny')]])
