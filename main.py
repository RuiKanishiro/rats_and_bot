from library import *
from name_translator import translation


def to_information(forecast: list):
    MONTHS = {'01': 'января', '02': 'февраля', '03': 'марта', '04': 'апреля', '05': 'мая', '06': 'июня',
              '07': 'июля', '08': 'августа', '09': 'сентября', '10': 'октября', '11': 'ноября', '12': 'декабря'}
    data = []
    cur_day = 0
    cur_month = ''
    for day in forecast:
        date = day['dt_txt']
        temp = int(day['main']['temp'])
        wind = int(day['wind']['speed'])
        description = day['weather'][0]['description']
        if int(date[8:10]) != cur_day:
            cur_day = int(date[8:10])
            cur_month = MONTHS[str(date[5:7])]
            data.append([f' • {cur_day} {cur_month}'])
        data[-1].append(f'{date[11:18]} - Температура: {temp}°C, {description}, ветер {wind} м/с')
    return data


def get_weather_forecast(api_key: str, city: str):
    try:
        url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric&lang=ru"

        response = requests.get(url)
        print(response.status_code)
        response.raise_for_status()

        weather_data = response.json()
        if weather_data and 'list' in weather_data:
            if weather_data and 'list' in weather_data:
                return weather_data['list']
            else:
                return "Нет данных о погоде."
    except requests.RequestException as e:
        return f"Такого города нет или случилось что-то ещё, попробуйте ещё раз\nОшибка {e}"
