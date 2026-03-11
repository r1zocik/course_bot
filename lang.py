# Все тексты бота на 3 языках
# ru = русский, uz = узбекский, en = английский

TEXTS = {
    "ru": {
        # Регистрация
        "welcome": (
            "👋 Добро пожаловать в <b>UzRate Bot</b>!\n\n"
            "Это бот для отслеживания курсов валют банков Узбекистана.\n\n"
            "Для начала пройдите регистрацию.\n\n"
            "📝 Введите ваше <b>имя</b>:"
        ),
        "welcome_back": "👋 С возвращением!\n\nВыберите действие:",
        "enter_name": "📝 Введите ваше имя:",
        "name_too_short": "❌ Имя слишком короткое. Попробуйте снова:",
        "share_phone": "✅ Отлично, <b>{name}</b>!\n\n📱 Нажмите кнопку ниже чтобы поделиться номером телефона:",
        "share_phone_btn": "📱 Отправить номер телефона",
        "reg_success": (
            "🎉 Регистрация прошла успешно!\n\n"
            "👤 Имя: <b>{name}</b>\n"
            "📱 Телефон: <b>{phone}</b>\n\n"
            "Теперь вы можете пользоваться всеми функциями бота! 🚀"
        ),
        # Меню
        "btn_convert": "💱 Конвертировать",
        "btn_banks": "🏦 Курсы банков",
        "btn_best": "📊 Лучшие курсы",
        "btn_profile": "ℹ️ Мой профиль",
        "btn_support": "📞 Поддержка",
        "btn_language": "🌐 Язык",
        "btn_back": "🔙 Назад",
        # Профиль
        "profile_title": "👤 <b>Ваш профиль</b>",
        "profile_name": "🙍 Имя",
        "profile_phone": "📱 Телефон",
        "profile_date": "📅 Регистрация",
        # Поддержка
        "support_text": (
            "📞 <b>Поддержка</b>\n\n"
            "Если у вас есть вопросы или проблемы — напишите администратору:\n\n"
            "👤 @admin_username\n\n"
            "Или опишите вашу проблему прямо здесь и мы свяжемся с вами."
        ),
        # Язык
        "choose_language": "🌐 Выберите язык / Tilni tanlang / Choose language:",
        "language_set": "✅ Язык изменён на Русский",
        # Общее
        "not_registered": "❌ Сначала пройдите регистрацию. Нажмите /start",
        "unknown_command": "❓ Не понял команду. Используйте кнопки меню:",
        "loading": "⏳ Загружаю актуальные курсы...",
    },

    "uz": {
        # Регистрация
        "welcome": (
            "👋 <b>UzRate Bot</b>ga xush kelibsiz!\n\n"
            "Bu bot O'zbekiston banklarining valyuta kurslarini kuzatish uchun.\n\n"
            "Boshlash uchun ro'yxatdan o'ting.\n\n"
            "📝 <b>Ismingizni</b> kiriting:"
        ),
        "welcome_back": "👋 Qaytib kelganingiz bilan!\n\nAmalni tanlang:",
        "enter_name": "📝 Ismingizni kiriting:",
        "name_too_short": "❌ Ism juda qisqa. Qaytadan urinib ko'ring:",
        "share_phone": "✅ Zo'r, <b>{name}</b>!\n\n📱 Telefon raqamingizni ulashish uchun quyidagi tugmani bosing:",
        "share_phone_btn": "📱 Telefon raqamini yuborish",
        "reg_success": (
            "🎉 Ro'yxatdan o'tish muvaffaqiyatli!\n\n"
            "👤 Ism: <b>{name}</b>\n"
            "📱 Telefon: <b>{phone}</b>\n\n"
            "Endi botning barcha funksiyalaridan foydalanishingiz mumkin! 🚀"
        ),
        # Меню
        "btn_convert": "💱 Konvertatsiya",
        "btn_banks": "🏦 Bank kurslari",
        "btn_best": "📊 Eng yaxshi kurslar",
        "btn_profile": "ℹ️ Mening profilim",
        "btn_support": "📞 Qo'llab-quvvatlash",
        "btn_language": "🌐 Til",
        "btn_back": "🔙 Orqaga",
        # Профиль
        "profile_title": "👤 <b>Sizning profilingiz</b>",
        "profile_name": "🙍 Ism",
        "profile_phone": "📱 Telefon",
        "profile_date": "📅 Ro'yxatdan o'tgan sana",
        # Поддержка
        "support_text": (
            "📞 <b>Qo'llab-quvvatlash</b>\n\n"
            "Savollaringiz yoki muammolaringiz bo'lsa — administratorga yozing:\n\n"
            "👤 @admin_username\n\n"
            "Yoki muammoingizni shu yerda tasvirlab bering, biz siz bilan bog'lanamiz."
        ),
        # Язык
        "choose_language": "🌐 Выберите язык / Tilni tanlang / Choose language:",
        "language_set": "✅ Til o'zgartirildi: O'zbek",
        # Общее
        "not_registered": "❌ Avval ro'yxatdan o'ting. /start ni bosing",
        "unknown_command": "❓ Buyruqni tushunmadim. Menyu tugmalaridan foydalaning:",
        "loading": "⏳ Joriy kurslar yuklanmoqda...",
    },

    "en": {
        # Регистрация
        "welcome": (
            "👋 Welcome to <b>UzRate Bot</b>!\n\n"
            "This bot tracks exchange rates of Uzbekistan banks.\n\n"
            "Please register to get started.\n\n"
            "📝 Enter your <b>name</b>:"
        ),
        "welcome_back": "👋 Welcome back!\n\nChoose an action:",
        "enter_name": "📝 Enter your name:",
        "name_too_short": "❌ Name is too short. Please try again:",
        "share_phone": "✅ Great, <b>{name}</b>!\n\n📱 Press the button below to share your phone number:",
        "share_phone_btn": "📱 Share phone number",
        "reg_success": (
            "🎉 Registration successful!\n\n"
            "👤 Name: <b>{name}</b>\n"
            "📱 Phone: <b>{phone}</b>\n\n"
            "You can now use all bot features! 🚀"
        ),
        # Меню
        "btn_convert": "💱 Convert",
        "btn_banks": "🏦 Bank rates",
        "btn_best": "📊 Best rates",
        "btn_profile": "ℹ️ My profile",
        "btn_support": "📞 Support",
        "btn_language": "🌐 Language",
        "btn_back": "🔙 Back",
        # Профиль
        "profile_title": "👤 <b>Your profile</b>",
        "profile_name": "🙍 Name",
        "profile_phone": "📱 Phone",
        "profile_date": "📅 Registered",
        # Поддержка
        "support_text": (
            "📞 <b>Support</b>\n\n"
            "If you have any questions or issues — contact the admin:\n\n"
            "👤 @admin_username\n\n"
            "Or describe your problem here and we will get back to you."
        ),
        # Язык
        "choose_language": "🌐 Выберите язык / Tilni tanlang / Choose language:",
        "language_set": "✅ Language changed to English",
        # Общее
        "not_registered": "❌ Please register first. Press /start",
        "unknown_command": "❓ Unknown command. Please use the menu buttons:",
        "loading": "⏳ Loading current rates...",
    }
}


def t(user_id: int, key: str, **kwargs) -> str:
    """Получить текст на языке пользователя."""
    from database.db import get_user_language
    lang = get_user_language(user_id)
    text = TEXTS.get(lang, TEXTS["ru"]).get(key, TEXTS["ru"].get(key, key))
    if kwargs:
        text = text.format(**kwargs)
    return text
