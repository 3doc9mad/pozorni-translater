import dearpygui.dearpygui as dpg


def get_split_index(msg):
    index = 45
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
        part_msg, rest_msg = put_split_msg(rest_msg, get_split_index(rest_msg))
        three_strings.append(part_msg)
    if len(three_strings) == 2:
        three_strings.append('\n')
    if rest_msg != '':
        three_strings[2] += '...'
    msg = ''
    for string_msg in three_strings:
        msg += string_msg + '\n'
    return msg


def send_recognize_text(text):
    dpg.set_value("recognize_text", get_short_message(text))


def send_translate_text(text):
    dpg.set_value("translate_text", get_short_message(text))


def send_status(status):
    statuses = {
        'listen': 'Слушаю Вас',
        'recognize': 'Разбираю речь',
        'translate': 'Перевожу',
        'text_to_speech': 'Синтезирую речь',
        'play_audio': 'Воспроизвожу речь',
    }
    dpg.set_value("status_text", statuses[status] + '...')



def log_message(message):
    message = message.encode('utf-8').decode('utf-8')
    print(message)
    dpg.set_value("log_text", dpg.get_value("log_text") + message + "\n")
