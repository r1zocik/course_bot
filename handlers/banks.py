from telebot import TeleBot
from telebot.types import Message
from database.db import is_registered
from keyboards.reply import main_menu_keyboard, banks_keyboard, currency_keyboard
from utils.rates import get_bank_rates, convert, format_number

bank_states = {}

STEP_BANK = "waiting_bank"
STEP_AMOUNT = "waiting_bank_amount"
STEP_CURRENCY = "waiting_bank_currency"

BANK_NAMES = {
    "🏦 Kapitalbank": "Kapitalbank",
    "🏦 Ipoteka Bank": "Ipoteka Bank",
    "🏦 Hamkorbank": "Hamkorbank",
    "🏦 Agrobank": "Agrobank",
    "🏦 NBU (Natsbank)": "NBU (Natsbank)",
}

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

    @bot.message_handler(func=lambda m: m.text == "🏦 Курсы банков")
    def start_banks(message: Message):
        user_id = message.from_user.id
        if not is_registered(user_id):
            bot.send_message(user_id, "❌ Сначала пройдите регистрацию. Нажмите /start")
            return

        bank_states[user_id] = {"step": STEP_BANK}
        bot.send_message(
            user_id,
            "🏦 <b>Курсы банков Узбекистана</b>\n\nВыберите банк:",
            parse_mode="HTML",
            reply_markup=banks_keyboard()
        )

    @bot.message_handler(func=lambda m: bank_states.get(m.from_user.id, {}).get("step") == STEP_BANK)
    def get_bank(message: Message):
        user_id = message.from_user.id

        if message.text == "🔙 Назад":
            del bank_states[user_id]
            bot.send_message(user_id, "Главное меню:", reply_markup=main_menu_keyboard())
            return

        bank = BANK_NAMES.get(message.text)
        if not bank:
            bot.send_message(user_id, "❌ Выберите банк из списка:", reply_markup=banks_keyboard())
            return

        bank_states[user_id]["bank"] = bank
        bank_states[user_id]["step"] = STEP_AMOUNT

        bot.send_message(
            user_id,
            f"✅ Банк: <b>{bank}</b>\n\nВведите сумму:",
            parse_mode="HTML"
        )

    @bot.message_handler(func=lambda m: bank_states.get(m.from_user.id, {}).get("step") == STEP_AMOUNT)
    def get_bank_amount(message: Message):
        user_id = message.from_user.id
        try:
            amount = float(message.text.replace(",", ".").replace(" ", ""))
            if amount <= 0:
                raise ValueError
        except ValueError:
            bot.send_message(user_id, "❌ Введите корректную сумму:")
            return

        bank_states[user_id]["amount"] = amount
        bank_states[user_id]["step"] = STEP_CURRENCY

        bot.send_message(
            user_id,
            f"Сумма: <b>{format_number(amount)}</b>\n\nВыберите <b>исходную валюту</b>:",
            parse_mode="HTML",
            reply_markup=currency_keyboard()
        )

    @bot.message_handler(func=lambda m: bank_states.get(m.from_user.id, {}).get("step") == STEP_CURRENCY)
    def get_bank_currency(message: Message):
        user_id = message.from_user.id

        if message.text == "🔙 Назад":
            bank_states[user_id]["step"] = STEP_AMOUNT
            bot.send_message(user_id, "Введите сумму снова:")
            return

        from_cur = CURRENCY_MAP.get(message.text)
        if not from_cur:
            bot.send_message(user_id, "❌ Выберите валюту из кнопок:", reply_markup=currency_keyboard())
            return

        state = bank_states[user_id]
        bank = state["bank"]
        amount = state["amount"]

        bot.send_message(user_id, "⏳ Загружаю актуальные курсы...")

        bank_rates, cbu_rates, full_info = get_bank_rates(bank)

        del bank_states[user_id]

        # Conversions
        lines = ""
        for to_cur in ["UZS", "RUB", "USD"]:
            if to_cur != from_cur:
                val = convert(amount, from_cur, to_cur, bank_rates)
                lines += f"  {CURRENCY_FLAGS[to_cur]} {to_cur}: <b>{format_number(val)}</b>\n"

        # Buy/sell rates for each currency
        rate_lines = ""
        for cur in ["USD", "RUB"]:
            info = full_info.get(cur, {})
            buy = format_number(info.get("buy", 0))
            sell = format_number(info.get("sell", 0))
            cbu_r = format_number(cbu_rates.get(cur, 0))
            source = info.get("source", "")
            source_label = "🌐" if source == "bank.uz" else "📊"
            rate_lines += (
                f"  {CURRENCY_FLAGS[cur]} {cur}: покупка <b>{buy}</b> | продажа <b>{sell}</b> {source_label}\n"
                f"  {'─'*20}\n"
                f"  ЦБ: {cbu_r} UZS\n\n"
            )

        bot.send_message(
            user_id,
            f"🏦 <b>{bank}</b>\n"
            f"{'─' * 25}\n"
            f"💰 {format_number(amount)} {CURRENCY_FLAGS[from_cur]} {from_cur}\n\n"
            f"📊 <b>Конвертация (курс продажи банка):</b>\n{lines}\n"
            f"📈 <b>Курсы {bank}:</b>\n{rate_lines}"
            f"🌐 = данные bank.uz  |  📊 = расчётный",
            parse_mode="HTML",
            reply_markup=main_menu_keyboard()
        )