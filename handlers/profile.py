from telebot import TeleBot
from telebot.types import Message
from database.db import is_registered, get_user
from keyboards.reply import main_menu_keyboard


def register_handlers(bot: TeleBot):

    @bot.message_handler(func=lambda m: m.text == "ℹ️ Мой профиль")
    def my_profile(message: Message):
        user_id = message.from_user.id
        if not is_registered(user_id):
            bot.send_message(user_id, "❌ Сначала пройдите регистрацию. Нажмите /start")
            return

        user = get_user(user_id)
        if user:
           _, name, phone, *_, registered_at = user
            bot.send_message(
                user_id,
                f"👤 <b>Ваш профиль</b>\n\n"
                f"{'─' * 25}\n"
                f"🙍 Имя: <b>{name}</b>\n"
                f"📱 Телефон: <b>{phone}</b>\n"
                f"📅 Регистрация: <b>{registered_at[:10]}</b>\n"
                f"{'─' * 25}",
                parse_mode="HTML",
                reply_markup=main_menu_keyboard()
            )
