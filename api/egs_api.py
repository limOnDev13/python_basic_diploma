"""Модуль, отвечающий за работу с api steam (https://rapidapi.com/1yesari1/api/epic-store-games)"""
from api.api_module import APIModule
from urllib.parse import urlencode
from typing import Callable, Optional, Any
from my_logging import info_logger
from loguru import logger


class EGSAPIModule(APIModule):
    """
    Класс, отвечающий за работу с API https://epic-store-games.p.rapidapi.com

    Args:
        request_length_limit (int) - Максимальная длина диапазона, по которому будет проводиться поиск.
        Если пользователь запросит вывести результат, который окажется длиннее заданного предела, то ему будет возвращен
        весь полученный список результатов. Например, если лимит будет установлен на 100 игр, пользователь попросит
        найти 200 игр с минимальной ценой, по его ключевому слову будет найдено 1000 игр, то программа просто выведет
        первые 200 игр из этого списка. Это реализованно для того, чтобы время ожидания было коротким.
    """
    def __init__(self, request_length_limit: int = 100):
        super().__init__(base_url='https://epic-store-games.p.rapidapi.com/onSale',
                         x_rapid_api_host="epic-store-games.p.rapidapi.com")
        self.lexicon['low'] = 'Пожалуйста, введите ключевое слово, по которому будут искаться самые дешевые игры'
        self.lexicon['high'] = 'Пожалуйста, введите ключевое слово, по которому будут искаться самые дорогие игры'
        self.lexicon['custom'] = ('Пожалуйста, введите ключевое слово,'
                                  ' по которому будут искаться игры в диапазоне, который вы укажите')
        self.lexicon['number'] = ('Пожалуйста, введите количество игр, которые вы хотите увидеть'
                                  ' (в данном api не более 40)')
        self.lexicon['range'] = 'Пожалуйста, введите ценовой диапазон (два числа через пробел)'
        self.lexicon['wrong number'] = 'Извините, я вас не понимаю... Пожалуйста, введите целое неотрицательное число'
        self.lexicon['wrong range'] = ('Извините, я вас не понимаю... Чтобы ввести ценовой диапазон, пожалуйста,'
                                       ' введите два числа через пробел')

        self.__req_len_limit: int = request_length_limit

    def __str__(self) -> str:
        return 'На данный момент бот работает с API https://rapidapi.com/1yesari1/api/epic-store-games, '\
               'который позволяет получать информацию о играх с магазина epic games store'

    def __get_response(self, *, product: str, number: int,
                       func_sort: Callable, func_filter: Optional[Callable[[Any], bool]] = None) -> str:
        """
        У методов low_api, high_api и custom_api код отличается только в методе сортировки и фильтре значений.
        Это функция несет в себе их общий функционал
        :param product: Ключевое слово, по которому проводится поиск
        :type product: str
        :param number: Количество запрашиваемых игр
        :param number: int
        :param func_sort: Функция сортировки
        :type func_sort: Callable
        :param func_filter: Функция фильтр
        :type func_filter: Optional[Callable]
        :return: Список запрашиваемых игр
        :rtype: str
        """
        query_string: str = urlencode({"searchWords": product,
                                       "categories": "Games",
                                       "locale": "ru",
                                       "country": "ru"})

        # Сделаем запрос
        list_games: list[dict] = self.request(
            url_request=self.base_url,
            query_string=query_string
        )
        # Отфильтруем значения
        if func_filter is not None:
            list_games = [game for game in list_games if func_filter(game)]

        # Выведем самые дешевые игры
        logger.warning(f'Метод __get_response пытается отфильтровать это\n{list_games}')
        try:
            list_games.sort(key=func_sort)
            list_games = list_games[:number]
            # Отсеем лишнюю информацию
            result_games: list[dict] = [
                {'title': game['title'],
                 'price': round(game['price']['totalPrice']['discountPrice'] / 100, 2),
                 'url': game['url']
                 }
                for game in list_games
            ]

            return self.__create_str_result(result_games)
        except AttributeError:
            logger.warning('Запрос успешно обработан, но результат не найден')
            return 'По вашему ключевому слову игры не найдены('

    @classmethod
    def __create_str_result(cls, response: list[dict]) -> str:
        """
        Метод переводит обработанный ответ сервера в строку
        :param response: Обработанный ответ сервера
        :type response: list[dict]
        :return: Строковый вид обработанного ответа сервера
        :rtype: str
        """
        result_string: str = '\n'.join(['{num}. {title} - {price} руб\nurl: {url}\n'.format(
            num=num + 1,
            title=game['title'],
            price=game['price'],
            url=game['url']
        ) for num, game in enumerate(response)])

        return result_string

    @info_logger(log_level='DEBUG', message='Запускается метод')
    def low_api(self, product: str, number: int) -> str:
        """
        Функция ищет игры по ключевому слову product и выводит number самых дешевых из них
        (если цены совпадают, то выводит первые попавшиеся)
        :param product: ключевое слово, по которому будут искаться игры
        :type product: str
        :param number: Количество игр с наименьшими ценами
        :type number: int
        :return: Список игр
        :rtype: list[dict]
        """
        return self.__get_response(
            product=product,
            number=number,
            func_sort=lambda game: game['price']['totalPrice']['discountPrice']
        )

    @info_logger(log_level='DEBUG', message='Запускается метод')
    def high_api(self, product: str, number: int) -> str:
        """
        Функция ищет игры по ключевому слову product и выводит number самых дорогих из них
        (если цены совпадают, то выводит первые попавшиеся)
        :param product: ключевое слово, по которому будут искаться игры
        :type product: str
        :param number: Количество игр с наименьшими ценами
        :type number: int
        :return: Список игр
        :rtype: list[dict]
        """
        return self.__get_response(
            product=product,
            number=number,
            func_sort=lambda game: -game['price']['totalPrice']['discountPrice']
        )

    @info_logger(log_level='DEBUG', message='Запускается метод')
    def custom_api(self, product: str, custom_range: tuple[float, float], number: int) -> str:
        """
        Функция ищет игры по ключевому слову product и выводит number шт по возрастанию в ценовом диапазоне custom_range
        (если цены совпадают, то выводит первые попавшиеся)
        :param product: ключевое слово, по которому будут искаться игры
        :type product: str
        :param custom_range: Ценовой диапазон
        :type custom_range: tuple[float, float]
        :param number: Количество игр с наименьшими ценами
        :type number: int
        :return: Список игр
        :rtype: list[dict]
        """
        return self.__get_response(
            product=product,
            number=number,
            func_sort=lambda game: game['price']['totalPrice']['discountPrice'],
            func_filter=lambda game:
            custom_range[0] <= game['price']['totalPrice']['discountPrice'] / 100 <= custom_range[1]
        )


if __name__ == '__main__':
    api: EGSAPIModule = EGSAPIModule()
    print(api.low_api('red dead', 5))
    print()
    print(api.high_api('red dead', 5))
    print()
    print(api.custom_api('red dead', (500, 2000), 5))
