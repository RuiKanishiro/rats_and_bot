# from library import *
#
#
# def get_weather_forecast(api_key: str, city: str):
#     MONTHS = {'01': 'января', '02': 'февраля', '03': 'марта', '04': 'апреля', '05': 'мая', '06': 'июня',
#               '07': 'июля', '08': 'августа', '09': 'сентября', '10': 'октября', '11': 'ноября', '12': 'декабря'}
#     try:
#         url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric&lang=ru"
#
#         response = requests.get(url)
#         response.raise_for_status()
#
#         weather_data = response.json()
#         if weather_data and 'list' in weather_data:
#             forecast = get_weather_forecast(api_key, city)
#
#             data = []
#             cur_day = 0
#             cur_month = ''
#             if isinstance(forecast, list):
#                 print(f"Прогноз погоды в городе {city}:")
#                 for day in forecast[:10]:
#                     date = day['dt_txt']
#                     temp = day['main']['temp']
#                     wind = day['wind']['speed']
#                     description = day['weather'][0]['description']
#                     if int(date[8:10]) != cur_day:
#                         cur_day = int(date[8:10])
#                         cur_month = MONTHS[day[5:7]]
#                         data.append([f'{cur_day} {cur_month}'])
#                     data[-1].append(f"{day[11:18]} - Температура: {temp}°C, {description}, ветер {wind} м/с")
#             return data
#         else:
#             return "Нет данных о погоде."
#     except requests.RequestException as e:
#         return f"Ошибка при выполнении запроса: {e}"