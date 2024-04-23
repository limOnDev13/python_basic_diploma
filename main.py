import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config_data import Config, load_config
from keyboards import set_main_menu
from handlers import standart_handlers, query_handlers
from database import start_database


async def main() -> None:
    """
    Основной скрипт телеграм бота
    :return: None
    """
    # Настройка основных параметров бота
    config: Config = load_config()
    bot: Bot = Bot(token=config.tg_bot.token,
                   parse_mode='HTML')
    storage: MemoryStorage = MemoryStorage()
    dp: Dispatcher = Dispatcher(storage=storage)

    # Запустим движок базы данных
    start_database()

    # вывод кнопки меню
    await set_main_menu(bot)

    # Регистрируем роутеры
    dp.include_routers(*[standart_handlers.router, query_handlers.router])

    # Удалим необработанные апдейты
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
