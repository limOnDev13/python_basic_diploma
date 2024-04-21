"""Модуль с ORM"""
import sqlalchemy as db
from sqlalchemy import Column
from sqlalchemy.orm import relationship, declarative_base


# Укажем, какую СУБД будем использовать
engine = db.create_engine('sqlite:///request_history.db')

# Создаем декларативный класс, от которого будут наследоваться все модели
Base = declarative_base()


class Requests(Base):
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

    __table_args__ = (
        db.PrimaryKeyConstraint('id', name='request_id'),
        db.UniqueConstraint('command', 'product', 'number', 'cus_range', name='unique_request')
    )  # В таблицу будут сохраняться только уникальные запросы

    results = relationship('Results')


class Results(Base):
    """
    Класс - модель, представляющая таблицу результатов на запросы.
    Связана по внешнему ключу с таблицей requests
    """
    __tablename__ = 'results'
    id = Column(db.Integer, autoincrement='auto')
    req_id = Column(db.Integer)
    seq_number = Column(db.Integer)
    product_title = Column(db.Text)
    amount = Column(db.REAL)
    meta = Column(db.Text)

    __table_args__ = (
        db.PrimaryKeyConstraint('id', name='result_id'),
        db.ForeignKeyConstraint(['req_id'], ['requests.id'])
    )


Base.metadata.create_all(engine)
