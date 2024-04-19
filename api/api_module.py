"""Модуль, в котором хранится базовый класс для работы со сторонним API.
Все другие модули должны наследоваться от этого класса"""
from abc import ABC, abstractmethod
import requests
from requests import Response
from config_data.config import Config, load_config
import time
from typing import Optional


class APIModule(ABC):
    """
    Базовый абстрактный класс для работы с API. Любые подключаемые модули с API должны наследоваться от этого класса

    Args:
        base_url (str): Базовый url, к которому будут отправляться запросы
        x_rapid_api_host (str): Хост rapidAPI
    """
    def __init__(self, base_url: str, x_rapid_api_host: str) -> None:
        self._base_url: str = base_url
        self._rapid_api_host: str = x_rapid_api_host
        self.lexicon: dict[str, Optional[str]] = {
            'low': None,
            'high': None,
            'custom': None,
            'number': None,
            'wrong number': None,
            'wrong range': None
        }

    @abstractmethod
    def __str__(self) -> str:
        pass

    @property
    def base_url(self) -> str:
        """Геттер для base_url"""
        return self._base_url

    @property
    def rapid_api_host(self) -> str:
        """Геттер для rapid_api_host"""
        return self._rapid_api_host

    @abstractmethod
    def low_api(self, product: str, number: int) -> str:
        """
        Запрос, при котором будут запрашиваться самые низкие цены / самые близкие места / самые доступные авто и т.д.
        :param product: Услуга/товар, по которым будет проводиться поиск
        :type product: str
        :param number:  Количество единиц категории (товаров/услуг)
        :type number: int
        :return: Результат запроса уже в строковом виде
        :rtype: str
        """
        pass

    @abstractmethod
    def high_api(self, product: str, number: int) -> str:
        """
        Запрос, при котором будут запрашиваться самая высокая стоимость,
        самые дорогие авто, самое удалённое местоположение и так далее
        :param product: Услуга/товар, по которым будет проводиться поиск
        :type product: str
        :param number:  Количество единиц категории (товаров/услуг)
        :type number: int
        :return: Результат запроса уже в строковом виде
        :rtype: list[dict]
        """
        pass

    @abstractmethod
    def custom_api(self, product: str, custom_range: tuple[float, float], number: int) -> str:
        """
        Вывод показателей пользовательского диапазона
        :param product: Услуга/товар, по которым будет проводиться поиск
        :type product: str
        :param custom_range: Диапазон значений выборки (цена от и до, расстояние от и до, срок от и до и так
        далее)
        :type custom_range: tuple[float, float]
        :param number:  Количество единиц категории (товаров/услуг)
        :type number: int
        :return: Результат запроса уже в строковом виде
        :rtype: str
        """
        pass

    def request(self, url_request: str, query_string: Optional[str] = None,
                key_word: Optional[str] = None, pause: int = 1) -> list[dict] | dict:
        """
        Метод делает полностью сформированный запрос по переданному url
        :param url_request: url запроса
        :type url_request: str
        :param query_string: url код словаря с параметрами
        :type query_string: Optional[str]
        :param key_word: Ключевое слово, которое отслеживается в ответе от сервера. В бесплатных api есть ограничение
        на количество запросов в секунду. Если в полученном ответе ключевое слово не найдено, значит,
        что этот лимит превышен и программа остановится на pause секунд
        :type key_word: Optional[str]
        :param pause: Время задержки запросов к серверу в случае задержки
        :type pause: int
        :return: Ответ на запрос
        :rtype: list[dict] | dict
        """
        config: Config = load_config()
        headers: dict[str, str] = {
            "X-RapidAPI-Key": config.api.rapidAPI_key,
            "X-RapidAPI-Host": self.rapid_api_host
        }

        while True:
            response: Response = requests.get(url_request, headers=headers, params=query_string)
            if isinstance(response.json(), dict) and (key_word is not None) and (key_word not in response):
                print('Превышена скорость запросов. Засыпаю на', pause, 'сек')
                time.sleep(pause)
            else:
                return response.json()

