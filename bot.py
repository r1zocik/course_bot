import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import telebot
from config import TOKEN
from database.db import init_db
from handlers import registration, converter, banks, profile, best_rates

bot = telebot.TeleBot(TOKEN, parse_mode=None)

# Initialize database
init_db()

# Register all handlers
registration.register_handlers(bot)
converter.register_handlers(bot)
banks.register_handlers(bot)
profile.register_handlers(bot)
best_rates.register_handlers(bot)


@bot.message_handler(func=lambda m: True)
def unknown(message):
    from database.db import is_registered
    from keyboards.reply import main_menu_keyboard
    if is_registered(message.from_user.id):
        bot.send_message(
            message.chat.id,
            "❓ Не понял команду. Используйте кнопки меню:",
            reply_markup=main_menu_keyboard()
        )
    else:
        bot.send_message(
            message.chat.id,
            "👋 Для начала работы нажмите /start"
        )


if __name__ == "__main__":
    print("✅ UzRate Bot запущен...")
    bot.infinity_polling()