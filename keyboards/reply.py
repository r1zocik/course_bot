from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


def main_menu_keyboard(user_id: int = None):
    from lang import t
    uid = user_id or 0

    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    kb.add(
        KeyboardButton(t(uid, "btn_convert")),
        KeyboardButton(t(uid, "btn_banks")),
        KeyboardButton(t(uid, "btn_best")),
        KeyboardButton("🗺 Обменники"),
        KeyboardButton(t(uid, "btn_profile")),
        KeyboardButton(t(uid, "btn_support")),
        KeyboardButton(t(uid, "btn_language")),
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