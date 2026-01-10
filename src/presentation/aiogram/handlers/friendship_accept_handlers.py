from aiogram import Router, F
from aiogram.types import CallbackQuery

from src.domain.services import IFriendshipService
from src.domain.dto.responses.friendship import AcceptFriendshipStatus
from src.domain.services.presentation import LexiconBase
from src.presentation.aiogram.keyboards.callbacks import FriendshipAcceptCallback
from src.presentation.aiogram.services import SendMenuService

router = Router()


@router.callback_query(FriendshipAcceptCallback.filter())
async def cb_friendship_accept(callback: CallbackQuery, callback_data: FriendshipAcceptCallback,
                               friendship_service: IFriendshipService,
                               send_menu_service: SendMenuService,
                               lexicon: LexiconBase):
    status: AcceptFriendshipStatus = \
        await friendship_service.accept_friendship(callback.from_user.id, callback_data.user_id)

    if status == AcceptFriendshipStatus.NotFound:
        await callback.answer(text=lexicon.get('friendship_request_not_found'),
                              show_alert=True)
    else:
        await callback.answer(text=lexicon.get('friendship_accepted_successful'))

    await send_menu_service.send_menu(callback.from_user.id, callback=callback)


@router.callback_query(F.data == 'friend_deny')
async def cb_friendship_deny(callback: CallbackQuery):
    await callback.message.delete()
