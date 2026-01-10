
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.domain.services.presentation import LexiconBase


def create_okay_kb(lexicon: LexiconBase) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=lexicon.get('kb_okay'), callback_data='close_it')]])
