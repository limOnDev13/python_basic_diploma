from dataclasses import dataclass
from environs import Env
from typing import Optional


@dataclass
class TgBot:
    """Класс для хранения токена бота"""
    token: str  # Токен для доступа к телеграм-боту


@dataclass
class API:
    rapidAPI_key: str


@dataclass
class Config:
    """Класс - конфиг"""
    tg_bot: TgBot
    api: API


def load_config(path: Optional[str] = None) -> Config:
    """
    Функция для загрузки данных из переменных окружения
    :param path: Путь до .env файла
    :type path: Optional[str]
    :return: объект Config с данными из окружения
    :rtype: Config
    """
    env: Env = Env()
    env.read_env(path)

    return Config(tg_bot=TgBot(token=env('BOT_TOKEN')),
                  api=API(rapidAPI_key=env('X-RapidAPI-Key')))
