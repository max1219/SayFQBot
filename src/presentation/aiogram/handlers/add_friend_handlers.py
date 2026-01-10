import logging

from aiogram import Router, F
from aiogram.types import Message

from src.domain.services.presentation import LexiconBase
from src.presentation.aiogram.keyboards.inline import create_okay_kb

from src.domain.services.interfaces.i_friendship_service import IFriendshipService
from src.domain.dto.responses.friendship import RequestFriendshipStatus

router = Router()

logger = logging.getLogger(__name__)


@router.message(F.users_shared)
async def process_user_shared(message: Message, friendship_service: IFriendshipService, lexicon: LexiconBase):
    status: RequestFriendshipStatus = \
        await friendship_service.request_friendship_by_id(message.from_user.id, message.users_shared.user_ids[0])

    logger.debug(
        f'Отправка заявки в друзья от {message.from_user.id} к {message.users_shared.user_ids[0]}. Статус: {status}')
    match status:
        case RequestFriendshipStatus.Success:
            await message.answer(
                text=lexicon.get('friendship_request_sent'), reply_markup=create_okay_kb(lexicon))
        case RequestFriendshipStatus.AlreadyRequested:
            await message.answer(
                text=lexicon.get('friendship_already_requested'))
        case RequestFriendshipStatus.AlreadyFriend:
            await message.answer(text=lexicon.get('friendship_already_friends'))
        case RequestFriendshipStatus.AutoAccepted:
            await message.answer(
                text=lexicon.get('friendship_auto_accept'))
        case RequestFriendshipStatus.UserNotFound:
            await message.answer(
                text=lexicon.get('friendship_user_not_found'))
        case RequestFriendshipStatus.CannotSendMessage:
            await message.answer(text=lexicon.get('friendship_cant_send_message'))
