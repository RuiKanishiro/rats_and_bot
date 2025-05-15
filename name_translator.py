from library import *


def translation(city: str):
    try:
        translator = Translator(from_lang="russian", to_lang="english")
        result = translator.translate(city)
        return result
    except RuntimeError as e:
        return f'Ошибка {e}'
