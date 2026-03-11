from telebot import TeleBot
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from database.db import is_registered
from keyboards.reply import main_menu_keyboard

# Обменники Ташкента с координатами
EXCHANGE_POINTS = [
    {
        "name": "Kapitalbank — Центр",
        "address": "ул. Амира Темура, 1, Ташкент",
        "lat": 41.2995,
        "lon": 69.2401,
        "hours": "09:00 - 18:00",
        "currencies": "USD, EUR, RUB",
    },
    {
        "name": "Ipoteka Bank — Центр",
        "address": "ул. Узбекистанская, 54, Ташкент",
        "lat": 41.3123,
        "lon": 69.2785,
        "hours": "09:00 - 17:00",
        "currencies": "USD, EUR, RUB",
    },
    {
        "name": "Hamkorbank — Чиланзар",
        "address": "ул. Катартол, 56, Ташкент",
        "lat": 41.2841,
        "lon": 69.2089,
        "hours": "09:00 - 18:00",
        "currencies": "USD, EUR, RUB",
    },
    {
        "name": "Agrobank — Юнусабад",
        "address": "пр. Амира Темура, 107, Ташкент",
        "lat": 41.3402,
        "lon": 69.2891,
        "hours": "09:00 - 17:30",
        "currencies": "USD, EUR, RUB",
    },
    {
        "name": "NBU — Главный офис",
        "address": "ул. Ислама Каримова, 6, Ташкент",
        "lat": 41.3056,
        "lon": 69.2760,
        "hours": "09:00 - 17:00",
        "currencies": "USD, EUR, RUB, GBP",
    },
    {
        "name": "Обменник — Аэропорт Ташкент",
        "address": "Ташкент Интернэшнл Аэропорт",
        "lat": 41.2579,
        "lon": 69.2813,
        "hours": "Круглосуточно",
        "currencies": "USD, EUR, RUB, GBP, CNY",
    },
    {
        "name": "Обменник — ТЦ Next",
        "address": "ул. Амира Темура, 21, Ташкент",
        "lat": 41.3001,
        "lon": 69.2711,
        "hours": "10:00 - 21:00",
        "currencies": "USD, EUR, RUB",
    },
    {
        "name": "Обменник — Бродвей",
        "address": "ул. Сайилгох, Ташкент",
        "lat": 41.2963,
        "lon": 69.2798,
        "hours": "09:00 - 20:00",
        "currencies": "USD, EUR, RUB",
    },
]


def exchange_map_keyboard():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(InlineKeyboardButton(
        "🗺 Открыть все на карте Google Maps",
        url="https://www.google.com/maps/search/обменник+валюты/@41.2995,69.2401,13z"
    ))
    kb.add(InlineKeyboardButton(
        "🗺 Открыть в Yandex Maps",
        url="https://yandex.uz/maps/10335/tashkent/?text=обмен+валюты"
    ))
    return kb


def register_handlers(bot: TeleBot):

    @bot.message_handler(func=lambda m: m.text in ["🗺 Обменники", "🗺 Обменники Ташкента"])
    def show_exchange_map(message: Message):
        user_id = message.from_user.id
        if not is_registered(user_id):
            bot.send_message(user_id, "❌ Сначала пройдите регистрацию. Нажмите /start")
            return

        # Отправляем список обменников
        text = "🗺 <b>Обменники Ташкента</b>\n\n"

        for i, point in enumerate(EXCHANGE_POINTS, 1):
            text += (
                f"<b>{i}. {point['name']}</b>\n"
                f"📍 {point['address']}\n"
                f"🕐 {point['hours']}\n"
                f"💱 {point['currencies']}\n\n"
            )

        bot.send_message(
            user_id,
            text,
            parse_mode="HTML",
            reply_markup=exchange_map_keyboard()
        )

        # Отправляем геолокации каждого обменника
        bot.send_message(user_id, "📍 <b>Геолокации на карте:</b>", parse_mode="HTML")

        for point in EXCHANGE_POINTS:
            bot.send_venue(
                user_id,
                latitude=point["lat"],
                longitude=point["lon"],
                title=point["name"],
                address=f"{point['address']} | {point['hours']}",
            )

        bot.send_message(
            user_id,
            "✅ Нажмите на любую точку чтобы открыть в картах!",
            reply_markup=main_menu_keyboard(user_id)
        )
