"""
Модуль с хэндлерами, отвечающими за обработку команд /low, /high, /custom и /history
"""
from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from lexicon import LEXICON_RU
from api import APIModule
# Необходимо импортировать модуль с выбранным api
from api import EGSAPIModule


api_module: EGSAPIModule = EGSAPIModule()
# Импортированный класс должен являться наследником от APIModule
if not isinstance(api_module, APIModule):
    raise SyntaxError('Импортированный модуль api не является сущностью APIModule!')

router: Router = Router()


@router.message(Command(commands=['low']))
async def process_start_command(message: Message) -> None:
    """
    Хэндлер для команды /low
    :param message: Объект сообщения пользователя
    :param message: Message
    :return: None
    """
    pass



