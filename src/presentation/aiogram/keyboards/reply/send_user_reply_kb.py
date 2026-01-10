from aiogram.utils.keyboard import KeyboardButton, KeyboardButtonRequestUsers, ReplyKeyboardMarkup

from src.domain.services.presentation import LexiconBase


def create_send_user_kb(lexicon: LexiconBase) -> ReplyKeyboardMarkup:
    buttons = [[
        KeyboardButton(text=lexicon.get('kb_friend_send'),
                       request_users=KeyboardButtonRequestUsers(
                           request_id=1,
                           user_is_bot=False,
                           max_quantity=1
                       ))]]

    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
