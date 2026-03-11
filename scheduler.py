import threading
import time
from datetime import datetime


def get_daily_message() -> str:
    """Формирует сообщение с актуальными курсами для рассылки."""
    from utils.rates import get_cbu_rates, format_number

    rates = get_cbu_rates()

    usd = format_number(rates.get("USD", 0))
    rub = format_number(rates.get("RUB", 0))
    eur = format_number(rates.get("EUR", 0))

    today = datetime.now().strftime("%d.%m.%Y")

    return (
        f"📅 <b>Курсы валют на {today}</b>\n"
        f"{'─' * 25}\n"
        f"🇺🇸 USD: <b>{usd} UZS</b>\n"
        f"🇷🇺 RUB: <b>{rub} UZS</b>\n"
        f"🇪🇺 EUR: <b>{eur} UZS</b>\n"
        f"{'─' * 25}\n"
        f"🏦 Источник: ЦБ Узбекистана\n\n"
        f"💱 Используйте кнопки меню для конвертации и курсов банков."
    )


def send_daily_rates(bot):
    """Отправляет курсы всем зарегистрированным пользователям."""
    from database.db import get_all_users

    print(f"⏰ Запуск ежедневной рассылки: {datetime.now().strftime('%H:%M:%S')}")

    users = get_all_users()
    message = get_daily_message()

    success = 0
    failed = 0

    for user_id, name in users:
        try:
            bot.send_message(user_id, message, parse_mode="HTML")
            success += 1
            time.sleep(0.05)  # небольшая пауза чтобы не спамить Telegram API
        except Exception as e:
            print(f"❌ Не удалось отправить {user_id} ({name}): {e}")
            failed += 1

    print(f"✅ Рассылка завершена: {success} успешно, {failed} ошибок")


def start_scheduler(bot, hour: int = 9, minute: int = 0):
    """
    Запускает фоновый поток который каждый день в указанное время
    отправляет курсы всем пользователям.
    
    hour, minute — время отправки по Ташкентскому времени (UTC+5).
    По умолчанию в 09:00.
    Render работает в UTC, поэтому 09:00 Ташкент = 04:00 UTC.
    """

    def run():
        print(f"📆 Планировщик запущен. Рассылка каждый день в {hour:02d}:{minute:02d} UTC")
        while True:
            now = datetime.utcnow()
            if now.hour == hour and now.minute == minute:
                send_daily_rates(bot)
                # Ждём 61 секунду чтобы не запустить дважды в одну минуту
                time.sleep(61)
            else:
                time.sleep(30)  # проверяем каждые 30 секунд

    thread = threading.Thread(target=run, daemon=True)
    thread.start()
