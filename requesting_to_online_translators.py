import requests

'''
Когда использовалась библиотека от гугл - была идея написать что-то своё для обращений к переводчикам
Задумка умерла от моей лени и от того, что этот велосипед уже был придуман
Оставил этот файл как дань памяти этой задумке (его можно удалить, если жалко 1.7kB памяти)
'''


def translate_text_with_yandex(api_key,
                               source_text: str,
                               source_language: str,
                               destination_language: str
                               ) -> str:
    url = "https://translate.yandex.net/api/v1.5/tr.json/translate"

    params = {
        "key": api_key,
        "text": source_text,
        "lang": f"{source_language}-{destination_language}"
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        return data["text"][0]
    else:
        return "Ошибка при переводе текста."


def translate_text_with_google(api_key, source_text: str, source_language: str, destination_language: str) -> str:
    url = "https://translation.googleapis.com/language/translate/v2"

    params = {
        "q": source_text,
        "source": source_language,
        "target": destination_language,
        "key": api_key
    }

    response = requests.get(url, params=params)
    data = response.json()

    if "data" in data and "translations" in data["data"]:
        return data["data"]["translations"][0]["translatedText"]
    else:
        return "Error: Unable to translate text."
