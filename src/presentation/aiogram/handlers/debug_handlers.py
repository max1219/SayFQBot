import logging

from typing import Sequence, Optional

from aiogram import Router
from aiogram.types import Message

from src.domain.dto.requests.user import AddUserRequest
from src.domain.dto.responses.user import GetUserResponse
from src.domain.services import IUserService, IFriendshipService, IFqService
from src.domain.services.interfaces.i_fq_limits_service import IFqLimitsService

from src.presentation.aiogram.filters import IsAdminFilter, CommandWithArgsFilter

router = Router()
router.message.filter(IsAdminFilter())
router.callback_query.filter(IsAdminFilter())


# User

@router.message(CommandWithArgsFilter('addUser'))
async def cmd_add_user(message: Message, args: Sequence[str],
                       user_service: IUserService):
    args: Optional[Sequence] = await CommandWithArgsFilter.check_and_process_args(
        message, args, [int, str], ['user_id', 'name'])
    if args is None:
        return
    status = await user_service.add_user(AddUserRequest(args[0], args[1]))
    await message.answer(str(status))


@router.message(CommandWithArgsFilter('removeUser'))
async def cmd_remove_user(message: Message, args: Sequence[str],
                          user_service: IUserService):
    args: Optional[Sequence] = await CommandWithArgsFilter.check_and_process_args(
        message, args, [int], ['user_id'])
    if args is None:
        return
    await user_service.remove_user(args[0])


@router.message(CommandWithArgsFilter('getAllUsers'))
async def cmd_get_all_users(message: Message, args: Sequence[str],
                            user_service: IUserService):
    if (await CommandWithArgsFilter.check_and_process_args(message, args, [], [])) is None:
        return
    users: Sequence[GetUserResponse] = await user_service.get_all_users()
    text = '\n'.join(map(lambda user: f'{user.user_id}:"{user.name}"', users))
    await message.answer(text)


@router.message(CommandWithArgsFilter('getUserById'))
async def cmd_get_user_by_id(message: Message, args: Sequence[str],
                             user_service: IUserService):
    args: Optional[Sequence] = await CommandWithArgsFilter.check_and_process_args(
        message, args, [int], ['user_id'])
    if not args:
        return
    user: GetUserResponse = await user_service.get_by_id(args[0])
    await message.answer(str(user))


@router.message(CommandWithArgsFilter('getUserByName'))
async def cmd_get_user_by_name(message: Message, args: Sequence[str],
                               user_service: IUserService):
    args: Optional[Sequence] = await CommandWithArgsFilter.check_and_process_args(
        message, args, [str], ['name'])
    if not args:
        return
    user: GetUserResponse = await user_service.get_by_name(args[0])
    await message.answer(str(user))


# Friendship

@router.message(CommandWithArgsFilter('getAllFriends'))
async def cmd_get_all_friends(message: Message, args: Sequence[str],
                              user_service: IUserService, friendship_service: IFriendshipService):
    args: Optional[Sequence] = await CommandWithArgsFilter.check_and_process_args(
        message, args, [int], ['user_id'])
    if not args:
        return
    friend_ids: Sequence[int] = await friendship_service.get_all_friends(args[0])
    friends: Sequence[GetUserResponse] = [await user_service.get_by_id(id_) for id_ in friend_ids]
    text = '\n'.join(map(lambda user: f'{user.user_id}:"{user.name}"', friends))
    await message.answer(text)


@router.message(CommandWithArgsFilter('requestFriendship'))
async def cmd_request_friendship(message: Message, args: Sequence[str],
                                 friendship_service: IFriendshipService):
    args: Optional[Sequence] = await CommandWithArgsFilter.check_and_process_args(
        message, args, [int, str], ['id_from', 'name_to'])
    if args is None:
        return
    status = await friendship_service.request_friendship(args[0], args[1])
    await message.answer(str(status))


@router.message(CommandWithArgsFilter('acceptFriendship'))
async def cmd_accept_friendship(message: Message, args: Sequence[str],
                                friendship_service: IFriendshipService):
    args: Optional[Sequence] = await CommandWithArgsFilter.check_and_process_args(
        message, args, [int, int], ['id_accepted', 'id_requested'])
    if args is None:
        return
    status = await friendship_service.accept_friendship(args[0], args[1])
    await message.answer(str(status))


@router.message(CommandWithArgsFilter('removeFriendship'))
async def cmd_remove_friendship(message: Message, args: Sequence[str],
                                friendship_service: IFriendshipService):
    args: Optional[Sequence] = await CommandWithArgsFilter.check_and_process_args(
        message, args, [int, int], ['user1_id', 'user2_id'])
    if args is None:
        return
    status = await friendship_service.remove_friendship(args[0], args[1])
    await message.answer(str(status))


@router.message(CommandWithArgsFilter('getIncomingFriendshipRequests'))
async def cmd_get_incoming_friendship_requests(message: Message, args: Sequence[str],
                                               friendship_service: IFriendshipService):
    args: Optional[Sequence] = await CommandWithArgsFilter.check_and_process_args(
        message, args, [int], ['user_to_id'])
    if args is None:
        return
    result = await friendship_service.get_incoming_requests(args[0])
    text = ', '.join(map(str, result))
    await message.answer(text)


# Fq

@router.message(CommandWithArgsFilter('sendFq'))
async def cmd_send_fq(message: Message, args: Sequence[str],
                      fq_service: IFqService):
    args: Optional[Sequence] = await CommandWithArgsFilter.check_and_process_args(
        message, args, [int, int], ['id_from', 'id_to'])
    if args is None:
        return
    status = await fq_service.send_fq(args[0], args[1])
    await message.answer(str(status))


@router.message(CommandWithArgsFilter('sendMeFq'))
async def cmd_send_me_fq(message: Message, args: Sequence[str],
                         fq_service: IFqService):
    args: Optional[Sequence] = await CommandWithArgsFilter.check_and_process_args(
        message, args, [int], ['id_from'])
    if args is None:
        return
    status = await fq_service.send_fq(args[0], message.from_user.id)
    await message.answer(str(status))


# Limits

@router.message(CommandWithArgsFilter('clearSpentLimits'))
async def cmd_clear_spent_limits(message: Message, args: Sequence[str],
                         fq_limits_service: IFqLimitsService):
    args: Optional[Sequence] = await CommandWithArgsFilter.check_and_process_args(
        message, args, [], [])
    if args is None:
        return
    await fq_limits_service.clear_spent_limits()
