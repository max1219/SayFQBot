
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton



def create_okay_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Ок, ясн', callback_data='okay')]])
