"""Модуль с ORM"""
import sqlalchemy as db
from sqlalchemy import Column
from sqlalchemy.orm import Session, declarative_base


# Укажем, какую СУБД будем использовать
__engine = db.create_engine('sqlite:///request_history.db')
# Создаем декларативный класс, от которого будут наследоваться все модели
__Base = declarative_base()


class Requests(__Base):
    """
    Класс - модель, представляющая таблицу запросов,
    где хранится информация о запросах пользователя. Согласно ТЗ, в ней можно хранить не более 10 записей
    """
    __tablename__ = 'requests'
    id = Column(db.Integer, autoincrement='auto')
    command = Column(db.Text, nullable=False)  # Команда
    product = Column(db.Text, nullable=False)  # Продукт
    number = Column(db.Integer, nullable=False)  # Количество продукта
    cus_range = Column(db.Text, nullable=True)  # Пользовательский диапазон
    result = Column(db.Text, nullable=True)

    __table_args__: tuple = (
        db.PrimaryKeyConstraint('id', name='request_id'),
    )


def start_database() -> None:
    """
    Метод запускает базу данных
    :return: None
    """
    __Base.metadata.create_all(__engine)


def get_session() -> Session:
    """
    Метод возвращает объект сессии
    :return: объект сессии
    :rtype: Session
    """
    return Session(bind=__engine)
