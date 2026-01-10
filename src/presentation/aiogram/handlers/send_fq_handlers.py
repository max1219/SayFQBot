from aiogram import Router
from aiogram.types import CallbackQuery

from src.domain.services import IFqService
from src.domain.dto.responses.fq import SendFqStatus
from src.domain.services.presentation import LexiconBase
from src.presentation.aiogram.keyboards.callbacks import FriendFqCallback
from src.presentation.aiogram.services import SendMenuService

router = Router()


@router.callback_query(FriendFqCallback.filter())
async def cb_friend_fq(callback: CallbackQuery, callback_data: FriendFqCallback,
                       fq_service: IFqService,
                       send_menu_service: SendMenuService,
                       lexicon: LexiconBase):
    status: SendFqStatus = await fq_service.send_fq(callback.from_user.id, callback_data.user_id)
    await send_menu_service.send_menu(callback.from_user.id, callback_data.page, callback)
    match status:
        case SendFqStatus.CannotSendMessage:
            await callback.answer(lexicon.get('fq_cant_send_message'),
                                  show_alert=True)
        case SendFqStatus.NotFriend:
            await callback.answer(lexicon.get('fq_not_friends'),
                                  show_alert=True)
        case SendFqStatus.UserNotFound:
            await callback.answer(lexicon.get('fq_user_not_found'),
                                  show_alert=True)
        case SendFqStatus.ToThisFriendLimitExceeded:
            await callback.answer(lexicon.get('fq_limit_to_exceeded'))
            await send_menu_service.send_menu(callback.from_user.id, callback_data.page, callback)
        case SendFqStatus.TotalLimitExceeded:
            await callback.answer(lexicon.get('fq_limit_total_exceeded'))
