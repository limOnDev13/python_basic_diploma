"""Модуль, отвечающий за работу с api steam (https://rapidapi.com/psimavel/api/steam2)
PS оказалось, что лимит запросов у этого API всего 10 запросов в минуту, поэтому не буду его заканчивать"""
from api_module import APIModule
from urllib.parse import urlencode


class SteamAPIModule(APIModule):
    """
    Класс, отвечающий за работу с API https://steam2.p.rapidapi.com

    Args:
        request_length_limit (int) - Максимальная длина диапазона, по которому будет проводиться поиск.
        Если пользователь запросит вывести результат, который окажется длиннее заданного предела, то ему будет возвращен
        весь полученный список результатов. Например, если лимит будет установлен на 100 игр, пользователь попросит
        найти 200 игр с минимальной ценой, по его ключевому слову будет найдено 1000 игр, то программа просто выведет
        первые 200 игр из этого списка. Это реализованно для того, чтобы время ожидания было коротким.
    """
    def __init__(self, request_length_limit: int = 100):
        super().__init__(base_url='https://steam2.p.rapidapi.com',
                         x_rapid_api_host="steam2.p.rapidapi.com")
        self.__req_len_limit: int = request_length_limit

    def low_api(self, product: str, number: int) -> list[dict]:
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
        # Переведем строку product в url код
        url_product: str = urlencode({'x': product})
        url_product = url_product[2:]

        # Сделаем запрос
        list_games: list[dict] = self.request(
            url_request='/'.join([self.base_url, 'search', url_product, 'page', '1'])
        )

        # В этом api чтобы узнать цену игры, придется переходить по каждой полученной ссылке
        for game in list_games:
            print(game)
            game['price'] = self.request(
                url_request='/'.join([self.base_url, 'appDetail', str(game['appId'])]),
                key_word='price',
                pause=2
            )['price']
            print()

        print(list_games)

    def high_api(self, product: str, number: int) -> list[dict]:
        return []

    def custom_api(self, product: str, custom_range: tuple[int, int], number: int) -> list[dict]:
        return []


if __name__ == '__main__':
    api: SteamAPIModule = SteamAPIModule()
    api.low_api('counter strike 2', 10)
