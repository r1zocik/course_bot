from telebot import TeleBot
from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton
from database.db import register_user, is_registered
from keyboards.reply import main_menu_keyboard, remove_keyboard

# Temporary storage for registration steps
user_states = {}  # {user_id: {"step": ..., "name": ...}}

STEP_NAME = "waiting_name"
STEP_PHONE = "waiting_phone"


def phone_request_keyboard():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb.add(KeyboardButton("📱 Отправить номер телефона", request_contact=True))
    return kb


def register_handlers(bot: TeleBot):

    @bot.message_handler(commands=["start"])
    def cmd_start(message: Message):
        user_id = message.from_user.id

        if is_registered(user_id):
            bot.send_message(
                user_id,
                f"👋 С возвращением!\n\nВыберите действие:",
                reply_markup=main_menu_keyboard()
            )
        else:
            user_states[user_id] = {"step": STEP_NAME}
            bot.send_message(
                user_id,
                "👋 Добро пожаловать в <b>UzRate Bot</b>!\n\n"
                "Это бот для отслеживания курсов валют банков Узбекистана.\n\n"
                "Для начала пройдите регистрацию.\n\n"
                "📝 Введите ваше <b>имя</b>:",
                parse_mode="HTML",
                reply_markup=remove_keyboard()
            )

    @bot.message_handler(func=lambda m: user_states.get(m.from_user.id, {}).get("step") == STEP_NAME)
    def get_name(message: Message):
        user_id = message.from_user.id
        name = message.text.strip()

        if len(name) < 2:
            bot.send_message(user_id, "❌ Имя слишком короткое. Попробуйте снова:")
            return

        user_states[user_id]["name"] = name
        user_states[user_id]["step"] = STEP_PHONE

        bot.send_message(
            user_id,
            f"✅ Отлично, <b>{name}</b>!\n\n"
            f"📱 Нажмите кнопку ниже чтобы поделиться номером телефона:",
            parse_mode="HTML",
            reply_markup=phone_request_keyboard()
        )

    # Handler for contact (button share)
    @bot.message_handler(content_types=["contact"])
    def get_phone_contact(message: Message):
        user_id = message.from_user.id

        if user_states.get(user_id, {}).get("step") != STEP_PHONE:
            return

        phone = message.contact.phone_number
        if not phone.startswith("+"):
            phone = "+" + phone

        name = user_states[user_id]["name"]
        register_user(user_id, name, phone)
        del user_states[user_id]

        bot.send_message(
            user_id,
            f"🎉 Регистрация прошла успешно!\n\n"
            f"👤 Имя: <b>{name}</b>\n"
            f"📱 Телефон: <b>{phone}</b>\n\n"
            f"Теперь вы можете пользоваться всеми функциями бота! 🚀",
            parse_mode="HTML",
            reply_markup=main_menu_keyboard()
        )