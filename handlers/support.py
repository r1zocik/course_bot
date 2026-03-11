from telebot import TeleBot
from telebot.types import Message
from database.db import is_registered
from keyboards.reply import main_menu_keyboard
from lang import t

# ⚠️ Замени на свой Telegram username администратора
ADMIN_USERNAME = "@mansurovpy"
ADMIN_USER_ID = None  # Можно указать числовой ID для пересылки сообщений


def register_handlers(bot: TeleBot):

    @bot.message_handler(func=lambda m: m.text in ["📞 Поддержка", "📞 Qo'llab-quvvatlash", "📞 Support"])
    def support(message: Message):
        user_id = message.from_user.id
        if not is_registered(user_id):
            bot.send_message(user_id, t(user_id, "not_registered"))
            return

        bot.send_message(
            user_id,
            f"📞 <b>{'Поддержка' if True else 'Support'}</b>\n\n"
            f"Если у вас есть вопросы — напишите администратору:\n\n"
            f"👤 {ADMIN_USERNAME}\n\n"
            f"─────────────────────────\n"
            f"<i>Или опишите вашу проблему ниже — мы свяжемся с вами.</i>",
            parse_mode="HTML",
            reply_markup=main_menu_keyboard(user_id)
        )
