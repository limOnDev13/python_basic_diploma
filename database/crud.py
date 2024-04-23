"""Модуль с CRUD операциями над бд"""
from sqlalchemy.sql import func
from sqlalchemy.orm import Session
from typing import Optional, Literal
from my_logging import info_logger

from database.orm import get_session, Requests


class CRUD:
    """
    Класс для исполнения RUD операций над базой данных
    """
    def __init__(self):
        self.__session: Session = get_session()  # Объект сессии

    @info_logger(log_level='DEBUG', message='Запускается метод')
    def read_all(self) -> Optional[list]:
        """
        Метод возвращает всю бд
        :return: бд
        :rtype: Optional[list[tuple]]
        """
        return self.__session.query(Requests.command,
                                    Requests.product,
                                    Requests.number,
                                    Requests.cus_range,
                                    Requests.result).all()

    @info_logger(log_level='DEBUG', message='Запускается метод')
    def read(self, command: Literal['low', 'high', 'custom'],
             product: str, number: int, cus_range: Optional[str] = None
             ) -> Optional[list]:
        """
        Метод ищет все строки в бд по введенной команде, продукту и его количеству (а также диапазону)
        и возвращает результат
        :param command: Команда
        :type command: Literal['low', 'high', 'custom']
        :param product: Продукт
        :type product: str
        :param number: Количество продукта
        :type number: int
        :param cus_range: Пользовательский диапазон
        :type cus_range: Optional[str]
        :return: Сохраненный результат этой команды. Если такой команды нет в бд, то None
        :rtype: Optional[str]
        """
        result_list: Optional[list] = self.__session.query(Requests.result).filter(
            Requests.command == command,
            Requests.product == product,
            Requests.number == number,
            Requests.cus_range == cus_range
        ).all()

        if len(result_list) == 0:
            return None
        else:
            return result_list

    @info_logger(log_level='DEBUG', message='Запускается метод')
    def create(self, command: Literal['low', 'high', 'custom'],
               product: str, number: int, cus_range: Optional[str],
               result: Optional[str], limit_requests: int = 10) -> None:
        """
        Метод добавляет в бд новый запрос и его результат
        :param command: Команда
        :type command: Literal['low', 'high', 'custom']
        :param product: Продукт
        :type product: str
        :param number: Количество продукта
        :type number: int
        :param cus_range: Пользовательский диапазон
        :type cus_range: Optional[str]
        :param result: Результат запроса
        :type result: Optional[str]
        :param limit_requests: Максимальное количество запросов, которые нужно хранить в бд.
        Согласно тз, лимит равен 10
        :param limit_requests: int
        :return: None
        """
        # Проверим количество сохраненных запросов в бд. Оно не должно превышать лимит
        num_requests: int = self.__session.query(Requests).count()
        if num_requests >= limit_requests:
            # Если бд уже заполнена, удалим старую запись, у нее наименьший первичный ключ
            min_prim_key: int = self.__session.query(func.min(Requests.id)).scalar()
            self.delete(min_prim_key)

        # Создадим запрос на добавление новой записи
        new_request: Requests = Requests(
            command=command,
            product=product,
            number=number,
            cus_range=cus_range,
            result=result
        )
        # Сделаем запрос
        self.__session.add(new_request)
        # Закоммитим
        self.__session.commit()

    @info_logger(log_level='DEBUG', message='Запускается метод')
    def delete(self, prim_key: int) -> None:
        """
        Метод удаляет по первичному ключу запрос из бд
        :param prim_key: Первичный ключ
        :type prim_key: int
        :return: None
        """
        # Создадим запрос
        delete_query = self.__session.query(Requests).filter(Requests.id == prim_key).one()
        # Сделаем запрос
        self.__session.delete(delete_query)
        # Закоммитим запрос
        self.__session.commit()


if __name__ == '__main__':
    from orm import start_database

    start_database()
    crud: CRUD = CRUD()

    # Проверка CRUD.create и CRUD.read
    crud.create('low', 'red', 10, None, '123')
    print(crud.read('low', 'red', 10, None))

    # Проверка переполнения CRUD.create
    for _ in range(11):
        crud.create('low', 'red', 10, None, '123')

    # Проверка read_all
    print(crud.read_all())
