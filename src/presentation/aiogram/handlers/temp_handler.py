import logging


from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from src.presentation.aiogram.services import SendMenuService
from src.presentation.aiogram.keyboards.callbacks import PageSelectCallback
from src.presentation.aiogram.keyboards.reply import create_send_user_kb

router = Router()


@router.message()
async def handler(message: Message, send_menu_service: SendMenuService):
    await message.answer(text='Welcome чел', reply_markup=create_send_user_kb())
    await send_menu_service.send_menu(message.from_user.id, 1)

@router.callback_query(PageSelectCallback.filter())
async def handle_callback(
        callback: CallbackQuery, callback_data: PageSelectCallback, send_menu_service: SendMenuService):
    await send_menu_service.send_menu(callback.from_user.id, callback_data.page, callback)