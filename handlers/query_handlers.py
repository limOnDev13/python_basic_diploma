"""
Модуль с хэндлерами, отвечающими за обработку команд /low, /high, /custom и /history
"""
from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from typing import Optional

from states import FSMQuery
from filters import IsDigit, IsRange
from lexicon import LEXICON_RU
from api import APIModule
from database import CRUD
# Необходимо импортировать модуль с выбранным api
from api import EGSAPIModule


# Чтобы подключить модуль с работой api, нужно изменить одну следующую строку
api_module: EGSAPIModule = EGSAPIModule()
# Импортированный класс должен являться наследником от APIModule
if not isinstance(api_module, APIModule):
    raise SyntaxError('Импортированный модуль api не является сущностью APIModule!')

router: Router = Router()
# Подцепим класс CRUD для работы с бд
crud: CRUD = CRUD()


@router.message(Command(commands=['history']), StateFilter(default_state))
async def process_history_command(message: Message) -> None:
    """
    Хэндлер, обрабатывающий команду /history в дефолтном состоянии
    :param message: Объект сообщения
    :type message: Message
    :return: None
    """
    # Получим историю запросов из бд
    history: list = crud.read_all()

    result_strings: list[str] = [
        '<b>Команда: {command}; продукт: {product};'
        ' количество: {number}; диапазон (если его нет, то None): {range}\n'
        'Результат:</b>\n{result}'.format(
            command=row[0],
            product=row[1],
            number=row[2],
            range=row[3],
            result=row[4]
        )
        for row in history
    ]
    await message.answer(text='\n'.join(result_strings))


@router.message(Command(commands=['low']), StateFilter(default_state))
async def process_low_command(message: Message, state: FSMContext) -> None:
    """
    Хэндлер для команды /low
    :param message: Объект сообщения пользователя
    :type message: Message
    :param state: Объект состояния
    :type state: FSMContext
    :return: None
    """
    await state.set_state(FSMQuery.fill_product)
    await state.update_data(command='low')
    await message.answer(text=api_module.lexicon['low'])


@router.message(Command(commands=['high']), StateFilter(default_state))
async def process_low_command(message: Message, state: FSMContext) -> None:
    """
    Хэндлер для команды /high
    :param message: Объект сообщения пользователя
    :type message: Message
    :param state: Объект состояния
    :type state: FSMContext
    :return: None
    """
    await state.set_state(FSMQuery.fill_product)
    await state.update_data(command='high')
    await message.answer(text=api_module.lexicon['high'])


@router.message(Command(commands=['custom']), StateFilter(default_state))
async def process_low_command(message: Message, state: FSMContext) -> None:
    """
    Хэндлер для команды /custom
    :param message: Объект сообщения пользователя
    :type message: Message
    :param state: Объект состояния
    :type state: FSMContext
    :return: None
    """
    await state.set_state(FSMQuery.fill_product)
    await state.update_data(command='custom')
    await message.answer(text=api_module.lexicon['custom'])


@router.message(StateFilter(FSMQuery.fill_product))
async def process_filling_product(message: Message, state: FSMContext) -> None:
    """
    Хэндлер для обработки ввода продукта
    :param message: Объект сообщения пользователя
    :type message: Message
    :param state: Объект состояния
    :type state: FSMContext
    :return: None
    """
    await state.update_data(product=message.text)

    data = await state.get_data()
    if data['command'] == 'custom':
        await state.set_state(FSMQuery.fill_range)
        await message.answer(text=api_module.lexicon['range'])
    else:
        await state.set_state(FSMQuery.fill_number)
        await state.update_data(range=None)
        await message.answer(text=api_module.lexicon['number'])


@router.message(StateFilter(FSMQuery.fill_range), IsRange())
async def process_start_command(message: Message, state: FSMContext, low_limit: int, high_limit: int) -> None:
    """
    Хэндлер для обработки ввода диапазона
    :param message: Объект сообщения пользователя
    :type message: Message
    :param state: Объект состояния
    :type state: FSMContext
    :param low_limit: Нижняя граница диапазона
    :type low_limit: int
    :param high_limit: Верхняя граница диапазона
    :type high_limit: int
    :return: None
    """
    await state.update_data(range=(low_limit, high_limit))
    await state.set_state(FSMQuery.fill_number)
    await message.answer(text=api_module.lexicon['number'])


@router.message(StateFilter(FSMQuery.fill_number), IsDigit())
async def process_start_command(message: Message, state: FSMContext) -> None:
    """
    Хэндлер для обработки ввода числа в состоянии ввода числа
    :param message: Объект сообщения пользователя
    :type message: Message
    :param state: Объект состояния
    :type state: FSMContext
    :return: None
    """
    await state.update_data(number=message.text)
    await state.set_state(default_state)

    data = await state.get_data()
    answer: Optional[str] = None

    if data['command'] == 'low':
        answer = api_module.low_api(product=data['product'], number=int(data['number']))
    elif data['command'] == 'high':
        answer = api_module.high_api(product=data['product'], number=int(data['number']))
    elif data['command'] == 'custom':
        answer = api_module.custom_api(product=data['product'], number=int(data['number']),
                                       custom_range=data['range'])

    if answer == '':
        answer = None
        await message.answer(text=LEXICON_RU['empty string'])
    else:
        await message.answer(text=answer)

    # Сохраним запрос с результатом в бд
    crud.create(command=data['command'],
                product=data['product'],
                cus_range=data['range'],
                number=data['number'],
                result=answer)


@router.message(StateFilter(FSMQuery.fill_number))
async def process_start_command(message: Message) -> None:
    """
    Хэндлер для обработки некорректного сообщения в состоянии ввода числа
    :param message: Объект сообщения пользователя
    :type message: Message
    :return: None
    """
    await message.answer(api_module.lexicon['wrong number'])


@router.message(StateFilter(FSMQuery.fill_range))
async def process_start_command(message: Message) -> None:
    """
    Хэндлер для обработки некорректного сообщения в состоянии ввода числа
    :param message: Объект сообщения пользователя
    :type message: Message
    :return: None
    """
    await message.answer(api_module.lexicon['wrong range'])


@router.message()
async def process_other_messages(message: Message) -> None:
    """
    Хэндлер, обрабатывающий все остальные сообщения
    :param message: объект Message
    :type message: Message
    :return: None
    """
    await message.answer(text=LEXICON_RU['other'])
