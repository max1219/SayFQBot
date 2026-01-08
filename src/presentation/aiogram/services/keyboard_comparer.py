from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup


def compare_inline_keyboards(kb1: InlineKeyboardMarkup, kb2: InlineKeyboardMarkup) -> bool:
    if len(kb1.inline_keyboard) != len(kb2.inline_keyboard):
        return False

    for row1, row2 in zip(kb1.inline_keyboard, kb2.inline_keyboard):
        if len(row1) != len(row2):
            return False

        for btn1, btn2 in zip(row1, row2):
            if btn1.text != btn2.text or btn1.callback_data != btn2.callback_data:
                return False

    return True


def compare_reply_keyboards(kb1: ReplyKeyboardMarkup, kb2: ReplyKeyboardMarkup) -> bool:
    if kb1.keyboard is None or kb2.keyboard is None:
        return kb1.keyboard == kb2.keyboard

    if len(kb1.keyboard) != len(kb2.keyboard):
        return False

    for row1, row2 in zip(kb1.keyboard, kb2.keyboard):
        if len(row1) != len(row2):
            return False

        for btn1, btn2 in zip(row1, row2):
            if btn1.text != btn2.text:
                return False

    if kb1.resize_keyboard != kb2.resize_keyboard:
        return False
    if kb1.one_time_keyboard != kb2.one_time_keyboard:
        return False

    return True
