from aiogram import Router, F
from aiogram.types import CallbackQuery

from src.domain.services import IFqService
from src.domain.dto.responses.fq import SendFqStatus
from src.presentation.aiogram.keyboards.callbacks import FriendFqCallback
from src.presentation.aiogram.services import SendMenuService

router = Router()


@router.callback_query(FriendFqCallback.filter())
async def cb_friend_fq(callback: CallbackQuery, callback_data: FriendFqCallback,
                 fq_service: IFqService, send_menu_service: SendMenuService):
    status: SendFqStatus = await fq_service.send_fq(callback.from_user.id, callback_data.user_id)

    match status:
        case SendFqStatus.Success:
            await send_menu_service.send_menu(callback.from_user.id, callback_data.page, callback)
        case SendFqStatus.CannotSendMessage:
            await callback.answer('Не удалось отправить сообщение. Возможно, эта х*ила добавила бота в чс',
                                  show_alert=True)
        case SendFqStatus.NotFriend:
            await callback.answer('Сообщение не отправлено, вы не друзья. Мб он удалил тебя из списка друзей',
                                  show_alert=True)
        case SendFqStatus.UserNotFound:
            await callback.answer('Сообщение не отправлено, юзер не найдет. Видимо, он удалил аккаунт в боте',
                                  show_alert=True)
        case SendFqStatus.ToThisFriendLimitExceeded:
            await callback.answer('Его путь уже назначен Вами. Повторите завтра')
            await send_menu_service.send_menu(callback.from_user.id, callback_data.page, callback)
        case SendFqStatus.TotalLimitExceeded:
            await callback.answer('На сегодня лимит исчерпан. Все, на кого вас не хватило, эту ночь спят спокойно')
