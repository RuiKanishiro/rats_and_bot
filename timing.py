from library import *
from name_translator import translation


def get_current_time(api_key, city):
    try:
        url = f"http://api.timezonedb.com/v2.1/get-time-zone?key={api_key}&format=json&by=zone&zone={city}"
        response = requests.get(url)
        response.raise_for_status()
        time_data = response.json()
        if time_data and 'formatted' in time_data:
            return time_data['formatted']
        else:
            return "Нет данных о времени."
    except requests.RequestException as e:
        return f"Ошибка при выполнении запроса: {e}"


def time_for_city(town: str):
    city = translation(town)
    stroke = city
    if city[:6] == 'Ошибка':
        stroke = stroke + '\n' + 'Похоже вы ввели название города некорректно'
        return stroke
    c = city.replace('-', '_')
    timezones = pytz.all_timezones
    for i in timezones:
        if c == i[i.rfind('/') + 1:]:
            current_time = get_current_time(api_key_zones, i)
            break
        else:
            current_time = 'Такого города нет'

    if current_time != 'Такого города нет':
        stroke = f"Текущее время в городе {town}: {current_time}"
    else:
        stroke = current_time
    return stroke
