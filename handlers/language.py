from telebot import TeleBot
from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton
from database.db import is_registered, set_user_language
from keyboards.reply import main_menu_keyboard
from lang import t

lang_states = {}


def language_keyboard():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    kb.add(
        KeyboardButton("🇷🇺 Русский"),
        KeyboardButton("🇺🇿 O'zbek"),
        KeyboardButton("🇬🇧 English"),
        KeyboardButton("🔙"),
    )
    return kb


LANG_MAP = {
    "🇷🇺 Русский": "ru",
    "🇺🇿 O'zbek": "uz",
    "🇬🇧 English": "en",
}


def register_handlers(bot: TeleBot):

    @bot.message_handler(func=lambda m: m.text in ["🌐 Язык", "🌐 Til", "🌐 Language"])
    def choose_language(message: Message):
        user_id = message.from_user.id
        if not is_registered(user_id):
            bot.send_message(user_id, t(user_id, "not_registered"))
            return

        lang_states[user_id] = True
        bot.send_message(
            user_id,
            t(user_id, "choose_language"),
            reply_markup=language_keyboard()
        )

    @bot.message_handler(func=lambda m: lang_states.get(m.from_user.id) and m.text in LANG_MAP)
    def set_language(message: Message):
        user_id = message.from_user.id
        lang = LANG_MAP[message.text]
        set_user_language(user_id, lang)
        lang_states.pop(user_id, None)

        bot.send_message(
            user_id,
            t(user_id, "language_set"),
            reply_markup=main_menu_keyboard(user_id)
        )

    @bot.message_handler(func=lambda m: lang_states.get(m.from_user.id) and m.text == "🔙")
    def back_from_language(message: Message):
        user_id = message.from_user.id
        lang_states.pop(user_id, None)
        bot.send_message(
            user_id,
            t(user_id, "welcome_back"),
            reply_markup=main_menu_keyboard(user_id)
        )
