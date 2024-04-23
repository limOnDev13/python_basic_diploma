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
    cur_msg_length: int = 0
    cur_msg: str = ''
    cur_num_strings: int = 0

    for string in response_list:
        # Перебираем все строки, пока не дойдем до максимальной длины сообщения в Телеграмме
        if cur_msg_length + len(string) < MAX_MSG_LENGTH - cur_num_strings:  # Строки будут соединяться с помощью \n
            cur_msg += '\n' + string
            cur_msg_length = len(cur_msg)
            cur_num_strings += 1
        elif cur_msg_length == 0 and len(string) >= MAX_MSG_LENGTH:
            # Если одна строка длиннее, чем максимальная длина - разбиваем ее на несколько сообщений
            while len(string) >= MAX_MSG_LENGTH:
                result_messages.append(string[:MAX_MSG_LENGTH - 1])
                string = string[MAX_MSG_LENGTH - 1:]
        else:
            # Если дошли до предела, то добавляем перечисленные строки в единую строку
            result_messages.append(cur_msg)
            cur_msg_length = 0
            cur_msg = ''
            cur_num_strings = 0

    return result_messages
