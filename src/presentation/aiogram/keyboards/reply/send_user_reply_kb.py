from aiogram.utils.keyboard import KeyboardButton, KeyboardButtonRequestUsers, ReplyKeyboardMarkup


def create_send_user_kb() -> ReplyKeyboardMarkup:
    buttons = [[
        KeyboardButton(text='Кинуть заявку в друзья',
                       request_users=KeyboardButtonRequestUsers(
                           request_id=1,
                           user_is_bot=False,
                           max_quantity=1
                       ))]]

    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
