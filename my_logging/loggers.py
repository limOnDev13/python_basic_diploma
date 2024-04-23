"""Модуль для логгирования"""
from loguru import logger
from typing import Callable, Any, Literal
import functools


def info_logger(log_level: Literal['CRITICAL', 'ERROR', 'SUCCESS', 'WARNING', 'INFO', 'DEBUG'],
                message: str) -> Callable:
    """
    Декоратор для логгирования
    :param log_level: Уровень логгирования
    :type log_level: Literal['CRITICAL', 'ERROR', 'SUCCESS', 'WARNING', 'INFO', 'DEBUG']
    :param message: Сообщение в лог
    :type message: str
    :return: Обернутую функцию
    :rtype: Callable
    """
    def log_wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            if log_level == 'CRITICAL':
                logger.critical('{name} - {message}'.format(name=func.__name__, message=message))
            elif log_level == 'ERROR':
                logger.error('{name} - {message}'.format(name=func.__name__, message=message))
            elif log_level == 'SUCCESS':
                logger.success('{name} - {message}'.format(name=func.__name__, message=message))
            elif log_level == 'WARNING':
                logger.warning('{name} - {message}'.format(name=func.__name__, message=message))
            elif log_level == 'INFO':
                logger.info('{name} - {message}'.format(name=func.__name__, message=message))
            elif log_level == 'DEBUG':
                logger.debug('{name} - {message}'.format(name=func.__name__, message=message))
                return func(*args, **kwargs)
        return wrapper
    return log_wrapper

