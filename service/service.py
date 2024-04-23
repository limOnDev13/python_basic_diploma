"""Модуль с вспомогательными функциями"""
MAX_MSG_LENGTH: int = 4096


def adjusting_length_message(response_list: list[str]) -> list[str]:
    """
    Метод получает список строк и красиво их компанует под максимальную длину сообщений телеграмма
    :param response_list: Список строк
    :type response_list: list[str]
    :return: Список сообщений
    :rtype: list[str]
    """
    result_messages: list[str] = list()
    current_message: list[str] = list()
    line_breaker_number: int = 0
    current_length: int = 0

    for string in response_list:
        if current_length + len(string) + line_breaker_number < MAX_MSG_LENGTH:
            # Если новая строка влезает в предел (с учетом переноса строки), то добавляем ее в текущее сообщение
            current_length += len(string) + 1
            line_breaker_number += 1
            current_message.append(string)
        else:
            if len(current_message) != 0:
                # Если мы достигли предела, то добавим в итоговый список сообщений все, что влезло
                result_messages.append('\n'.join(current_message))

            # Текущая string может превышать предел длины сообщений
            if len(string) > MAX_MSG_LENGTH:
                # Будем разбивать string на несколько сообщений
                while len(string) > 0:
                    result_messages.append(string[:MAX_MSG_LENGTH])
                    string = string[MAX_MSG_LENGTH:]
                line_breaker_number = 0
                current_message = list()
                current_length = 0
            else:
                # Иначе все обнуляем
                line_breaker_number = 1
                current_message = [string]
                current_length = len(string) + 1

    # Последние string могли не достигнуть предела, поэтому их отдельно нужно добавить в результатные сообщения
    if len(current_message) != 0:
        result_messages.append('\n'.join(current_message))

    return result_messages
