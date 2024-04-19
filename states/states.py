"""
Модуль с классами, отражающими возможные состояния пользователя.
"""
from aiogram.filters.state import StatesGroup, State


class FSMQuery(StatesGroup):
    fill_product: State = State()
    fill_number: State = State()
    fill_range: State = State()
