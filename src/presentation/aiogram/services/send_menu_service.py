from typing import Sequence, Optional

from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, CallbackQuery

from src.domain.services import IUserService, IFriendshipService, IFqLimitsService

from src.presentation.aiogram.keyboards import create_main_kb
from src.presentation.aiogram.keyboards.types import FriendEntry, PaginationData


class SendMenuService:
    def __init__(self,
                 user_service: IUserService,
                 friendship_service: IFriendshipService,
                 fq_limits_service: IFqLimitsService,
                 n_friends_on_page,
                 bot: Bot):
        self._user_service = user_service
        self._friendship_service = friendship_service
        self._fq_limits_service = fq_limits_service
        self._n_friends_on_page = n_friends_on_page
        self._bot = bot


    async def send_menu(self, user_id: int, page: int, callback: Optional[CallbackQuery] = None) -> None:
        """
        :param user_id:
        :param page:
        :param callback: Если None, отправляет новое сообщение, иначе редактирует старое
        :return:
        """
        friend_ids: Sequence[int] = await self._friendship_service.get_all_friends(user_id)
        pagination_data: Optional[PaginationData] = None
        if len(friend_ids) > self._n_friends_on_page:
            total_pages = (len(friend_ids) - 1) // self._n_friends_on_page + 1
            friend_ids = friend_ids[(page - 1) * self._n_friends_on_page: page * self._n_friends_on_page]
            pagination_data = PaginationData(
                current_page=page,
                total_pages=total_pages)

        friend_names: Sequence[str] = [(await self._user_service.get_by_id(friend_id)).name for friend_id in friend_ids]
        friend_sent_flags: Sequence[bool] = [
            (await self._fq_limits_service.get_to_this_friend_limit_spent(user_id, friend_id)) == 1
            for friend_id in friend_ids]
        friend_entries = map(lambda triple: FriendEntry(user_id=triple[0], name=triple[1], is_already_sent=triple[2]),
                             zip(friend_ids, friend_names, friend_sent_flags))


        keyboard: InlineKeyboardMarkup = create_main_kb(friend_entries, pagination_data)

        text = "Пашла нахуй шваль"
        if callback:
            if callback.message.text != text:
                await callback.message.edit_text(text=text, reply_markup=keyboard)
            elif callback.message.reply_markup != keyboard:
                await callback.message.edit_reply_markup(reply_markup=keyboard)
        else:
            await self._bot.send_message(chat_id=user_id, text=text, reply_markup=keyboard)
