import logging

from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message

from src.presentation.aiogram.keyboards.reply import create_send_user_kb

from src.domain.services.interfaces.i_friendship_service import IFriendshipService
from src.domain.dto.responses.friendship import RequestFriendshipStatus

router = Router()

logger = logging.getLogger(__name__)


@router.callback_query(F.data == 'friend_search')
async def cb_friend_search(callback: CallbackQuery, bot: Bot):
    await callback.message.delete()
    await bot.send_message(chat_id=callback.from_user.id,
                           text='Кинь, кого хочешь позвать. Он должен быть зареган в боте',
                           reply_markup=create_send_user_kb())


@router.message(F.users_shared)
async def process_user_shared(message: Message, friendship_service: IFriendshipService):
    status: RequestFriendshipStatus = \
        await friendship_service.request_friendship_by_id(message.from_user.id, message.users_shared.user_ids[0])

    logger.debug(
        f'Отправка заявки в друзья от {message.from_user.id} к {message.users_shared.user_ids[0]}. Статус: {status}')
    match status:
        case RequestFriendshipStatus.Success:
            await message.answer(text='Заявка в друзья отправлена. Можете пригласить еще кого')
        case RequestFriendshipStatus.AlreadyRequested:
            await message.answer(
                text='Ты уже кидал ему заявку. Он либо отклонил, либо проигнорил. Пусть кинет ответную, она будет принята автоматически')
        case RequestFriendshipStatus.AlreadyFriend:
            await message.answer(text='Вы с ним уже друзья')
        case RequestFriendshipStatus.AutoAccepted:
            await message.answer(
                text='Он уже кидал тебе заявку, так что твоя была принята автоматически. Теперь вы друзья, шли его каждый день, чтобы не забывал, куда ему дорога')
        case RequestFriendshipStatus.UserNotFound:
            await message.answer(
                text='Не знаю такого. Пусть напишет мне. Кинь на меня ссылку')
        case RequestFriendshipStatus.CannotSendMessage:
            await message.answer(
                text='Не могу написать ему. Возможно, эта шваль кинула меня в чс')
