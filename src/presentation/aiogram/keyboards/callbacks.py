from aiogram.filters.callback_data import CallbackData

class BaseCbWithReturnMenu(CallbackData, prefix='OVERRIDE ME'):
    page: int

class FriendSelectCallback(BaseCbWithReturnMenu, prefix='friend_select'):
    user_id: int

class FriendFqCallback(BaseCbWithReturnMenu, prefix='friend_fq'):
    user_id: int

class PageSelectCallback(CallbackData, prefix='page_select'):
    page: int

class FriendshipAcceptCallback(CallbackData, prefix='friend_accept'):
    user_id: int