"""
Модуль со стандартными хэндлерами
"""
from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from lexicon import LEXICON_RU

router: Router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message) -> None:
    """
    Хэндлер для команды /start
    :param message: Объект сообщения пользователя
    :param message: Message
    :return: None
    """
    await message.answer(text=LEXICON_RU['start'])


@router.message(Command(commands=['help']))
async def process_help_command(message: Message) -> None:
    """
    Хэндлер для команды /help
    :param message: Объект сообщения пользователя
    :param message: Message
    :return: None
    """
    await message.answer(text=LEXICON_RU['help'])
