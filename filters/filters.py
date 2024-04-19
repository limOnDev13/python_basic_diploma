from aiogram.filters import BaseFilter
from aiogram.types import Message


class IsDigit(BaseFilter):
    """Класс фильтр, пропускает, если сообщение - это число"""
    async def __call__(self, message: Message) -> bool:
        return message.text.isdigit() and int(message.text) >= 0


class IsRange(BaseFilter):
    """Класс фильтр, пропускает, если сообщение - это два числа через пробел"""
    async def __call__(self, message: Message) -> bool | dict[str, int]:
        numbers_str: list[str] = message.text.split()

        if len(numbers_str) != 2:
            return False

        if not numbers_str[0].isdigit() or not numbers_str[1].isdigit():
            return False
        return {'low_limit': int(numbers_str[0]), 'high_limit': int(numbers_str[1])}
