from telebot import TeleBot
from telebot.types import Message
from database.db import is_registered
from keyboards.reply import main_menu_keyboard, currency_keyboard
from utils.rates import get_rates, convert, format_number

# States for conversion flow
convert_states = {}  # {user_id: {"step": ..., "amount": ..., "from_currency": ...}}

STEP_AMOUNT = "waiting_amount"
STEP_FROM = "waiting_from_currency"
STEP_TO = "waiting_to_currency"

CURRENCY_MAP = {
    "🇺🇿 UZS": "UZS",
    "🇷🇺 RUB": "RUB",
    "🇺🇸 USD": "USD",
}

CURRENCY_FLAGS = {
    "UZS": "🇺🇿",
    "RUB": "🇷🇺",
    "USD": "🇺🇸",
}


def register_handlers(bot: TeleBot):

    @bot.message_handler(func=lambda m: m.text == "💱 Конвертировать")
    def start_convert(message: Message):
        user_id = message.from_user.id
        if not is_registered(user_id):
            bot.send_message(user_id, "❌ Сначала пройдите регистрацию. Нажмите /start")
            return

        convert_states[user_id] = {"step": STEP_AMOUNT}
        bot.send_message(
            user_id,
            "💱 <b>Конвертация валют</b>\n\n"
            "Введите сумму для конвертации:",
            parse_mode="HTML"
        )

    @bot.message_handler(func=lambda m: convert_states.get(m.from_user.id, {}).get("step") == STEP_AMOUNT)
    def get_amount(message: Message):
        user_id = message.from_user.id
        try:
            amount = float(message.text.replace(",", ".").replace(" ", ""))
            if amount <= 0:
                raise ValueError
        except ValueError:
            bot.send_message(user_id, "❌ Введите корректную сумму (например: 100 или 1500.50):")
            return

        convert_states[user_id]["amount"] = amount
        convert_states[user_id]["step"] = STEP_FROM

        bot.send_message(
            user_id,
            f"✅ Сумма: <b>{format_number(amount)}</b>\n\n"
            f"Выберите <b>исходную валюту</b>:",
            parse_mode="HTML",
            reply_markup=currency_keyboard()
        )

    @bot.message_handler(func=lambda m: convert_states.get(m.from_user.id, {}).get("step") == STEP_FROM)
    def get_from_currency(message: Message):
        user_id = message.from_user.id

        if message.text == "🔙 Назад":
            del convert_states[user_id]
            bot.send_message(user_id, "Главное меню:", reply_markup=main_menu_keyboard())
            return

        currency = CURRENCY_MAP.get(message.text)
        if not currency:
            bot.send_message(user_id, "❌ Выберите валюту из кнопок ниже:", reply_markup=currency_keyboard())
            return

        convert_states[user_id]["from_currency"] = currency
        convert_states[user_id]["step"] = STEP_TO

        bot.send_message(
            user_id,
            f"Исходная валюта: <b>{CURRENCY_FLAGS[currency]} {currency}</b>\n\n"
            f"Теперь выберите <b>валюту назначения</b>:",
            parse_mode="HTML",
            reply_markup=currency_keyboard()
        )

    @bot.message_handler(func=lambda m: convert_states.get(m.from_user.id, {}).get("step") == STEP_TO)
    def get_to_currency(message: Message):
        user_id = message.from_user.id

        if message.text == "🔙 Назад":
            convert_states[user_id]["step"] = STEP_FROM
            bot.send_message(user_id, "Выберите исходную валюту:", reply_markup=currency_keyboard())
            return

        currency = CURRENCY_MAP.get(message.text)
        if not currency:
            bot.send_message(user_id, "❌ Выберите валюту из кнопок ниже:", reply_markup=currency_keyboard())
            return

        state = convert_states[user_id]
        amount = state["amount"]
        from_cur = state["from_currency"]
        to_cur = currency

        rates = get_rates()
        result = convert(amount, from_cur, to_cur, rates)

        del convert_states[user_id]

        # Show all rates for reference
        all_results = ""
        for cur in ["UZS", "RUB", "USD"]:
            if cur != from_cur:
                val = convert(amount, from_cur, cur, rates)
                all_results += f"  {CURRENCY_FLAGS[cur]} {cur}: <b>{format_number(val)}</b>\n"

        bot.send_message(
            user_id,
            f"💱 <b>Результат конвертации</b>\n\n"
            f"{'─' * 25}\n"
            f"💰 {format_number(amount)} {CURRENCY_FLAGS[from_cur]} {from_cur}\n"
            f"➡️ <b>{format_number(result)} {CURRENCY_FLAGS[to_cur]} {to_cur}</b>\n"
            f"{'─' * 25}\n\n"
            f"📊 Также:\n{all_results}\n"
            f"📅 Курс ЦБ Узбекистана (актуальный)",
            parse_mode="HTML",
            reply_markup=main_menu_keyboard()
        )