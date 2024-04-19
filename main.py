import asyncio
from aiogram import Bot, Dispatcher

from config_data import Config, load_config


async def main():
    # Настройка основных параметров бота
    config: Config = load_config()
    bot: Bot = Bot(token=config.tg_bot.token,
                   parse_mode='HTML')
    dp: Dispatcher = Dispatcher()

    # Удалим необработанные апдейты
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
