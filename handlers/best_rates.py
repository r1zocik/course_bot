from telebot import TeleBot
from telebot.types import Message
from database.db import is_registered
from keyboards.reply import main_menu_keyboard
from utils.rates import get_bank_rates, format_number

BANKS = [
    "Kapitalbank",
    "Ipoteka Bank",
    "Hamkorbank",
    "Agrobank",
    "NBU (Natsbank)",
]

CURRENCY_FLAGS = {
    "USD": "🇺🇸",
    "RUB": "🇷🇺",
}


def register_handlers(bot: TeleBot):

    @bot.message_handler(func=lambda m: m.text in ["📊 Лучшие курсы", "📊 Eng yaxshi kurslar", "📊 Best rates"])
    def best_rates(message: Message):
        user_id = message.from_user.id
        if not is_registered(user_id):
            bot.send_message(user_id, "❌ Сначала пройдите регистрацию. Нажмите /start")
            return

        msg = bot.send_message(user_id, "⏳ Собираю курсы всех банков, подождите...")

        all_data = {}
        for bank in BANKS:
            try:
                bank_rates, cbu_rates, full_info = get_bank_rates(bank)
                all_data[bank] = full_info
            except Exception as e:
                print(f"Error fetching {bank}: {e}")
                all_data[bank] = {}

        result = ""

        for cur in ["USD", "RUB"]:
            flag = CURRENCY_FLAGS[cur]

            best_buy_bank = None
            best_buy_val = -1
            best_sell_bank = None
            best_sell_val = float("inf")
            worst_buy_bank = None
            worst_buy_val = float("inf")
            worst_sell_bank = None
            worst_sell_val = -1

            rows = []
            for bank, info in all_data.items():
                cur_info = info.get(cur, {})
                buy = cur_info.get("buy", 0)
                sell = cur_info.get("sell", 0)
                source = cur_info.get("source", "")
                source_icon = "🌐" if "themoney" in source else "📊"

                if buy > 0 and sell > 0:
                    rows.append((bank, buy, sell, source_icon))

                    if buy > best_buy_val:
                        best_buy_val = buy
                        best_buy_bank = bank
                    if sell < best_sell_val:
                        best_sell_val = sell
                        best_sell_bank = bank
                    if buy < worst_buy_val:
                        worst_buy_val = buy
                        worst_buy_bank = bank
                    if sell > worst_sell_val:
                        worst_sell_val = sell
                        worst_sell_bank = bank

            result += f"{flag} <b>{cur} / UZS</b>\n"
            result += f"{'─' * 28}\n"
            result += f"{'Банк':<18} {'Покупка':>9} {'Продажа':>9}\n"

            for bank, buy, sell, icon in rows:
                short = bank.replace(" (Natsbank)", "").replace(" Bank", "")
                buy_str = format_number(buy)
                sell_str = format_number(sell)
                result += f"{icon} {short:<16} {buy_str:>9} {sell_str:>9}\n"

            result += f"\n"

            if best_buy_bank:
                result += (
                    f"✅ <b>Лучшая покупка (вы продаёте):</b>\n"
                    f"   🏆 {best_buy_bank} — <b>{format_number(best_buy_val)} UZS</b>\n\n"
                    f"✅ <b>Лучшая продажа (вы покупаете):</b>\n"
                    f"   🏆 {best_sell_bank} — <b>{format_number(best_sell_val)} UZS</b>\n\n"
                    f"❌ <b>Дороже всего купить у:</b>\n"
                    f"   💸 {worst_sell_bank} — <b>{format_number(worst_sell_val)} UZS</b>\n\n"
                )

            result += f"{'═' * 28}\n\n"

        result += "🌐 = данные themoney.uz  |  📊 = расчётный\n"
        result += "💡 <i>Лучшая покупка = банк даёт больше UZS за вашу валюту\nЛучшая продажа = банк продаёт дешевле всех</i>"

        bot.delete_message(user_id, msg.message_id)
        bot.send_message(
            user_id,
            f"📊 <b>Сравнение курсов всех банков</b>\n\n{result}",
            parse_mode="HTML",
            reply_markup=main_menu_keyboard(user_id)
        )
