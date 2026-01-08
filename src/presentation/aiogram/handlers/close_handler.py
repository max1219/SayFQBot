from aiogram import Router, F
from aiogram.types import CallbackQuery


router = Router()

@router.callback_query(F.data == 'close_it')
async def cb_close(callback: CallbackQuery):
    await callback.message.delete()
