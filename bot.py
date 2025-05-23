import asyncio
import datetime

from library import *
from timing import get_current_time, time_for_city
from main import to_information, get_weather_forecast
from name_translator import translation


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
menu_keyboard = ReplyKeyboardMarkup([['/today', '/for5days'], ['/time', '/start'], ['/help']], resize_keyboard=True, one_time_keyboard=True)
other_city_keyboard = ReplyKeyboardMarkup([['/today', '/for5days'], ['/time', '/help']], resize_keyboard=True, one_time_keyboard=True)
register_keyboard = ReplyKeyboardMarkup([['/register']], resize_keyboard=True, one_time_keyboard=True)
start_keyboard = ReplyKeyboardMarkup([['/start']], resize_keyboard=True, one_time_keyboard=True)
user_data = {'LOCAL_CITY': '',
             'DATETIME': '',
             'NAME': ''
             }
CURRENT_CITY = ''
CHAT_ID = ''


async def send_periodic_message(update: Update, context: CallbackContext) -> None:
    while True:
        time_now = datetime.datetime.now()
        minutes = time_now.minute
        hours = time_now.hour
        data_minutes = int(user_data['DATETIME'][user_data['DATETIME'].find(':') + 1:])
        data_hours = int(user_data['DATETIME'][:user_data['DATETIME'].find(':')])
        if data_hours == int(hours) and data_minutes == int(minutes):
            sticker = 'CAACAgIAAxkBAAEPGkhoJR_7FlasLoSVRyQlzKpaei_duQAC5ScAAnjYIUv9gmRGJesDATYE'
            await update.message.reply_sticker(sticker)
            await update.message.reply_text(f"Ёмаё, уже {user_data['DATETIME']}")
            await predict_for_today(update, context)
            await asyncio.sleep(3600)
        await asyncio.sleep(30)


async def start(update: Update, context: CallbackContext) -> None:
    if user_data['LOCAL_CITY'] == '' or user_data['DATETIME'] == '' or user_data['NAME'] == '':
        CHAT_ID = update.message.chat_id
        sticker = "CAACAgIAAxkBAAEPGj1oJRrz8ksvf-OZJ3X027ije0j8uAACeCEAApwcgEqM13Cb64xqPzYE"
        await update.message.reply_sticker(sticker)
        await update.message.reply_text(
            'Йоу! Это смешной штука, который может делать что-то\nЧтобы познать все возможности этого бота, давайте зарегистрируем вас, путник',
            reply_markup=register_keyboard
        )
    else:
        asyncio.create_task(send_periodic_message(update, context))
        sticker = "CAACAgIAAxkBAAEPGj9oJRtDFfeVAz0aKNkZJkjwYIHLVgACeR0AAuwzgUolnQABxqkDfMI2BA"
        await update.message.reply_sticker(sticker)
        await update.message.reply_text(
            'Йоу! Вы авторизованы. Теперь вам доступно много функций! По вопросам, связанными с функциями, вы можете обратится в функцию /help, которая лежит в меню:',
            reply_markup=menu_keyboard
        )


async def registration(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Как я могу вас звать?')
    return 1


async def get_name(update: Update, context: CallbackContext):
    user_data['NAME'] = update.message.text
    await update.message.reply_text(
        f"Хорошо, {user_data['NAME']}!\nВ каком городе вы живете? Пишите на русском с большой буквы"
    )
    return 2


async def get_city(update: Update, context: CallbackContext):
    user_data['LOCAL_CITY'] = update.message.text
    await update.message.reply_text(
        f"В какое время мне отправлять вам прогноз погоды г. {user_data['LOCAL_CITY']}?\nПишите часы и минуты через :, к примеру 15:00"
    )
    return 3


async def get_time(update: Update, context: CallbackContext):
    user_data['DATETIME'] = update.message.text
    sticker = "CAACAgIAAxkBAAEPGkZoJRvJnG51EN6wuUcHiDmb3R7nSAAC0S8AAtIUIUt5i2pb2ydpQjYE"
    await update.message.reply_sticker(sticker)
    await update.message.reply_text(
        f"Отлично! Заполнение данных окончено.\nНажмите /start ещё раз :)",
        reply_markup=start_keyboard
    )


async def cancel(update: Update, context: CallbackContext):
    await update.message.reply_text('Регистрация отменена.')
    user_data['NAME'] = ''
    user_data['LOCAL_CITY'] = ''
    user_data['DATETIME'] = datetime
    return ConversationHandler.END


# async def canceling(update: Update, context: CallbackContext):
#     await update.message.reply_text('пупупу')
#     CURRENT_CITY = ''
#     return ConversationHandler.END


async def predict_for_today(update: Update, context: CallbackContext):
    global CURRENT_CITY
    if CURRENT_CITY == '':
        c_answ = user_data['LOCAL_CITY']
        city = translation(user_data['LOCAL_CITY']).lower()
    else:
        c_answ = CURRENT_CITY
        city = translation(CURRENT_CITY).lower()
    stroke_answ = ''
    if city[:6] == 'Ошибка':
        stroke_answ = stroke_answ + '\n' + 'Похоже вы ввели название города некорректно'
    else:
        information = get_weather_forecast(api_key_weather, city)
        if isinstance(information, list):
            information = to_information(information)

        if isinstance(information, list):
            stroke_answ = f"Прогноз погоды в городе {user_data['LOCAL_CITY']} на сегодня:" + '\n'
            for i in information[0]:
                stroke_answ = stroke_answ + i + '\n'
    await update.message.reply_text(stroke_answ, reply_markup=menu_keyboard)
    CURRENT_CITY = ''


async def predict_all(update: Update, context: CallbackContext):
    global CURRENT_CITY
    if CURRENT_CITY == '':
        c_answ = user_data['LOCAL_CITY']
        city = translation(user_data['LOCAL_CITY']).lower()
    else:
        c_answ = CURRENT_CITY
        city = translation(CURRENT_CITY).lower()
    stroke_answ = ''
    if city[:6] == 'Ошибка':
        stroke_answ = stroke_answ + '\n' + 'Похоже вы ввели название города некорректно'
    else:
        information = get_weather_forecast(api_key_weather, city)
        if isinstance(information, list):
            information = to_information(information)

        if isinstance(information, list):
            stroke_answ = f"Прогноз погоды в городе {c_answ}:" + '\n'
            for i in information:
                for j in i:
                    stroke_answ = stroke_answ + j + '\n'
    await update.message.reply_text(stroke_answ, reply_markup=menu_keyboard)
    CURRENT_CITY = ''


# async def other_city(update: Update, context: CallbackContext):
#     await update.message.reply_text("Введите название города, погоду или время в котором вы хотите узнать", reply_markup=other_city_keyboard)
#     return 1


# async def get_other_city(update: Update, context: CallbackContext):
#     CURRENT_CITY = update.message.text
#     await update.message.reply_text(f'Супер! Давайте узнаем что-то о городе {CURRENT_CITY}', reply_markup=other_city_keyboard)
#     return ConversationHandler.END


async def time_(update: Update, context: CallbackContext):
    global CURRENT_CITY
    answer = 'Что-то пошло не так....\nЯ попробую ещё раз'
    k = 0
    while answer == 'Что-то пошло не так....\nЯ попробую ещё раз' and k < 10:
        if CURRENT_CITY == '':
            answer = time_for_city(translation(user_data['LOCAL_CITY']), user_data['LOCAL_CITY'])
        else:
            answer = time_for_city(translation(CURRENT_CITY), CURRENT_CITY)
        k += 1
    if k == 10:
        answer = 'Я очень сожалею, но у меня не получилось :('
    await update.message.reply_text(answer)


async def help_me(update: Update, context: CallbackContext):
    await update.message.reply_text("-Ты хоть знаешь чей я сын?\n-Чей же?\n-Божий. Приходите к нам на службу в пятницу.")
    sticker = "CAACAgIAAxkBAAEPGjdoJRaUJvsgxaU-BXKwWMZ8O4M3jwAClwADzxzAJU77Coy6YW8VNgQ"
    await update.message.reply_sticker(sticker)
    await update.message.reply_text(f"Имя: {user_data['NAME']}\nГород по умолчанию: {user_data['LOCAL_CITY']}\nВремя ежедневного прогноза погоды по умолчанию: {user_data['DATETIME']}")
    await update.message.reply_text("Кнопка /time выводит время в городе по умолчанию или в написанном городе, если нажата после кнопки /other_city")
    await update.message.reply_text("Кнопка /today выводит погоду на сегодня в городе по умолчанию или в написанном городе, если нажата после кнопки /other_city")
    await update.message.reply_text("Кнопка /for5days выводит ближайший известный прогноз погоды в городе по умолчанию или в написанном городе, если нажата после кнопки /other_city")
    await update.message.reply_text("Кнопка /other_city позволяет узнать информацию о городе, название которого вы введёте, но в данный момент она не работает по техническим причинам")


def main() -> None:
    application = Application.builder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler(['register'], registration)],
        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            2: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_city)],
            3: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_time)],
        },
        fallbacks=[CommandHandler(['cancel'], cancel)],
    )

    application.add_handler(CommandHandler(["start"], start))
    application.add_handler(CommandHandler(["today"], predict_for_today))
    application.add_handler(CommandHandler(["for5days"], predict_all))
    application.add_handler(CommandHandler(["help"], help_me))
    application.add_handler(CommandHandler(["time"], time_))
    application.add_handler(conv_handler)

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()