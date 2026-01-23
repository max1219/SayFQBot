
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.domain.services.presentation import LexiconBase

from src.presentation.aiogram.keyboards.callbacks import ResponseFqCallback


def create_response_fq_kb(user_to_id: int, lexicon: LexiconBase) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(
            text=lexicon.get('kb_fq_response'),
            callback_data=ResponseFqCallback(user_id=user_to_id).pack())]])
