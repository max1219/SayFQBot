from aiogram import Router, F
from aiogram.types import CallbackQuery, Message


router = Router()

@router.callback_query(F.data == 'okay')
async def cb_okay(callback: CallbackQuery):
    await callback.message.delete()
