from telebot import TeleBot
from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton
from database.db import is_registered, get_user
from keyboards.reply import main_menu_keyboard, currency_keyboard
from utils.rates import get_rates, convert, format_number

convert_states = {}

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


def receipt_keyboard():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    kb.add(
        KeyboardButton("🧾 Скачать чек"),
        KeyboardButton("🔙 Главное меню"),
    )
    return kb


def register_handlers(bot: TeleBot):

    @bot.message_handler(func=lambda m: m.text in ["💱 Конвертировать", "💱 Konvertatsiya", "💱 Convert"])
    def start_convert(message: Message):
        user_id = message.from_user.id
        if not is_registered(user_id):
            bot.send_message(user_id, "❌ Сначала пройдите регистрацию. Нажмите /start")
            return

        convert_states[user_id] = {"step": STEP_AMOUNT}
        bot.send_message(
            user_id,
            "💱 <b>Конвертация валют</b>\n\nВведите сумму для конвертации:",
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
            f"✅ Сумма: <b>{format_number(amount)}</b>\n\nВыберите <b>исходную валюту</b>:",
            parse_mode="HTML",
            reply_markup=currency_keyboard()
        )

    @bot.message_handler(func=lambda m: convert_states.get(m.from_user.id, {}).get("step") == STEP_FROM)
    def get_from_currency(message: Message):
        user_id = message.from_user.id

        if message.text == "🔙 Назад":
            del convert_states[user_id]
            bot.send_message(user_id, "Главное меню:", reply_markup=main_menu_keyboard(user_id))
            return

        currency = CURRENCY_MAP.get(message.text)
        if not currency:
            bot.send_message(user_id, "❌ Выберите валюту из кнопок ниже:", reply_markup=currency_keyboard())
            return

        convert_states[user_id]["from_currency"] = currency
        convert_states[user_id]["step"] = STEP_TO

        bot.send_message(
            user_id,
            f"Исходная валюта: <b>{CURRENCY_FLAGS[currency]} {currency}</b>\n\nТеперь выберите <b>валюту назначения</b>:",
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

        # Считаем курс
        if from_cur == "UZS":
            rate = 1 / rates.get(to_cur, 1)
        elif to_cur == "UZS":
            rate = rates.get(from_cur, 1)
        else:
            rate = rates.get(from_cur, 1) / rates.get(to_cur, 1)

        # Сохраняем результат для чека
        convert_states[user_id] = {
            "step": "done",
            "amount": amount,
            "from_cur": from_cur,
            "to_cur": to_cur,
            "result": result,
            "rate": rate,
        }

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
            reply_markup=receipt_keyboard()
        )

    @bot.message_handler(func=lambda m: m.text == "🧾 Скачать чек")
    def send_receipt(message: Message):
        user_id = message.from_user.id
        state = convert_states.get(user_id, {})

        if state.get("step") != "done":
            bot.send_message(user_id, "❌ Сначала выполните конвертацию.", reply_markup=main_menu_keyboard(user_id))
            return

        user = get_user(user_id)
        user_name = user[1] if user else "Пользователь"

        bot.send_message(user_id, "⏳ Генерирую чек...")

        try:
            from utils.receipt import generate_receipt_pdf
            pdf_bytes = generate_receipt_pdf(
                user_name=user_name,
                amount=state["amount"],
                from_cur=state["from_cur"],
                to_cur=state["to_cur"],
                result=state["result"],
                rate=state["rate"],
            )

            from datetime import datetime
            filename = f"receipt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

            bot.send_document(
                user_id,
                (filename, pdf_bytes),
                caption="🧾 Ваш чек конвертации готов!",
                reply_markup=main_menu_keyboard(user_id)
            )
        except Exception as e:
            print(f"Receipt error: {e}")
            bot.send_message(user_id, "❌ Ошибка при создании чека.", reply_markup=main_menu_keyboard(user_id))

        del convert_states[user_id]

    @bot.message_handler(func=lambda m: m.text == "🔙 Главное меню")
    def back_to_menu(message: Message):
        user_id = message.from_user.id
        convert_states.pop(user_id, None)
        bot.send_message(user_id, "Главное меню:", reply_markup=main_menu_keyboard(user_id))