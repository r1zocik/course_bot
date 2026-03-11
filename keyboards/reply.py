from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


def main_menu_keyboard():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    kb.add(
        KeyboardButton("💱 Конвертировать"),
        KeyboardButton("🏦 Курсы банков"),
        KeyboardButton("📊 Лучшие курсы"),
        KeyboardButton("ℹ️ Мой профиль"),
    )
    return kb


def banks_keyboard():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    banks = [
        "🏦 Kapitalbank",
        "🏦 Ipoteka Bank",
        "🏦 Hamkorbank",
        "🏦 Agrobank",
        "🏦 NBU (Natsbank)",
        "🔙 Назад",
    ]
    for bank in banks:
        kb.add(KeyboardButton(bank))
    return kb


def currency_keyboard():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    kb.add(
        KeyboardButton("🇺🇿 UZS"),
        KeyboardButton("🇷🇺 RUB"),
        KeyboardButton("🇺🇸 USD"),
        KeyboardButton("🔙 Назад"),
    )
    return kb


def remove_keyboard():
    return ReplyKeyboardRemove()