import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import telebot
from config import TOKEN
from database.db import init_db
from handlers import registration, converter, banks, profile, best_rates, language, support, exchange_map
from scheduler import start_scheduler

bot = telebot.TeleBot(TOKEN, parse_mode=None)

# Initialize database
init_db()

# Register all handlers
registration.register_handlers(bot)
converter.register_handlers(bot)
banks.register_handlers(bot)
profile.register_handlers(bot)
best_rates.register_handlers(bot)
language.register_handlers(bot)
support.register_handlers(bot)
exchange_map.register_handlers(bot)

# Запуск ежедневной рассылки в 09:00 по Ташкенту (04:00 UTC)
start_scheduler(bot, hour=4, minute=0)


@bot.message_handler(func=lambda m: True)
def unknown(message):
    from database.db import is_registered
    from keyboards.reply import main_menu_keyboard
    from lang import t
    user_id = message.from_user.id
    if is_registered(user_id):
        bot.send_message(
            message.chat.id,
            t(user_id, "unknown_command"),
            reply_markup=main_menu_keyboard(user_id)
        )
    else:
        bot.send_message(
            message.chat.id,
            "👋 Для начала работы нажмите /start"
        )


if __name__ == "__main__":
    print("✅ UzRate Bot запущен...")
    bot.infinity_polling()