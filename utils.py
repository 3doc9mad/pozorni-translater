import json
import random
import string

import dearpygui.dearpygui as dpg


def get_split_index(msg):
    index = 49
    print(len(msg))
    char = msg[index]
    while char != ' ':
        index -= 1
        char = msg[index]
    return index


def put_split_msg(msg, index):
    return msg[:index], msg[index + 1:]


def get_short_message(msg):
    if len(msg) <= 50:
        return msg + '\n\n\n'
    else:
        rest_msg = msg
    three_strings = []

    while len(three_strings) < 3:
        if len(rest_msg) > 50:
            part_msg, rest_msg = put_split_msg(rest_msg, get_split_index(rest_msg))
        else:
            part_msg = rest_msg
            rest_msg = ''
        three_strings.append(part_msg)
    if len(three_strings) == 2:
        three_strings.append('\n')
    if rest_msg != '':
        three_strings[2] += '...'
    msg = ''
    for string_msg in three_strings:
        msg += string_msg + '\n'
    return msg


with open('config.json', 'r') as config_file:
    config = json.load(config_file)


def get_config():
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
        return config


def send_recognize_text(text):
    dpg.set_value("recognize_text", get_short_message(text))


def send_translate_text(text):
    dpg.set_value("translate_text", get_short_message(str(text)))


def send_status(status):
    statuses = {
        'loading': 'Загрузка',
        'listen': 'Слушаю Вас',
        'recognize': 'Разбираю речь',
        'translate': 'Перевожу',
        'text_to_speech': 'Синтезирую речь',
        'play_audio': 'Воспроизвожу речь',
    }

    if status == 'listen':
        dpg.configure_item('main_button', texture_tag='mic-fill', enabled=True)
    else:
        dpg.configure_item('main_button', texture_tag='mic', enabled=False)
    dpg.set_value("status_text", statuses[status] + '...')


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def log_message(message):
    message = message.encode('utf-8').decode('utf-8')
    print(message)
    if message is None:
        message = 'Nothing'
    dpg.set_value("log_text", dpg.get_value("log_text") + message + "\n")
