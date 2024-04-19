import asyncio
from aiogram import Bot, Dispatcher

from config_data import Config, load_config
from keyboards import set_main_menu
from handlers import standart_handlers


async def main() -> None:
    """
    Основной скрипт телеграм бота
    :return: None
    """
    # Настройка основных параметров бота
    config: Config = load_config()
    bot: Bot = Bot(token=config.tg_bot.token,
                   parse_mode='HTML')
    dp: Dispatcher = Dispatcher()

    # вывод кнопки меню
    await set_main_menu(bot)

    # Регистрируем роутеры
    dp.include_routers(*[standart_handlers.router])

    # Удалим необработанные апдейты
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
