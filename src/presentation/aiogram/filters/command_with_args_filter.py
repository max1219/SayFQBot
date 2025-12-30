

from typing import Any, Sequence, Optional, Type, TypeGuard

from aiogram.filters import BaseFilter
from aiogram.types import Message


class CommandWithArgsFilter(BaseFilter):
    def __init__(self, command: str):
        self._prefix = f'/{command}'

    async def __call__(self, message: Message) -> bool | dict[str, Any]:
        if message.text is None or not message.text.startswith(self._prefix):
            return False

        parts = message.text.split()

        return {'command': parts[0], 'args': parts[1:]}

    @staticmethod
    async def check_and_process_args(
            message: Message, args: Sequence[str], types: Sequence[Type], arg_names: Sequence[str]) -> Optional[
        Sequence]:
        """
        Проверяет корректность аргументов (количество, типы).
        Если есть ошибка, отправляет сообщение о неверных типах и возвращает None.
        Если ошибок нет, возвращает приведенные к нужным типам аргументы.
        Работает только с int, str
        """

        def get_interface_str() -> str:
            if len(types) == 0:
                return 'без аргументов'
            return '  '.join(map(lambda pair: f'{pair[0]}:({pair[1].__name__})', zip(arg_names, types)))

        if len(args) != len(types):
            interface_str = get_interface_str()
            await message.answer(f'Неверное количество аргументов.\nИнтерфейс команды: {interface_str}.')
            return None

        result = []
        for arg, type_, name in zip(args, types, arg_names):
            if type_ == int:
                if not str.isdigit(arg):
                    interface_str = get_interface_str()
                    await message.answer(f'Неверный тип аргумента {name}.\nИнтерфейс команды: {interface_str}.')
                    return None
                result.append(int(arg))
            elif type_ == str:
                result.append(arg)
            else:
                raise Exception('Недопустимый тип для проверки')

        return result