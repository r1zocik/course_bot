import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "users.db")


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            language TEXT DEFAULT 'ru',
            registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # Добавить колонку language если её нет (для старых баз)
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN language TEXT DEFAULT 'ru'")
    except Exception:
        pass
    conn.commit()
    conn.close()


def register_user(user_id: int, name: str, phone: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR REPLACE INTO users (user_id, name, phone, language) VALUES (?, ?, ?, COALESCE((SELECT language FROM users WHERE user_id=?), 'ru'))",
        (user_id, name, phone, user_id)
    )
    conn.commit()
    conn.close()


def get_user(user_id: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return row


def is_registered(user_id: int) -> bool:
    return get_user(user_id) is not None


def get_all_users():
    """Возвращает список всех зарегистрированных пользователей."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, name FROM users")
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_user_language(user_id: int) -> str:
    """Возвращает язык пользователя (ru/uz/en)."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT language FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else "ru"


def set_user_language(user_id: int, language: str):
    """Устанавливает язык пользователя."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET language = ? WHERE user_id = ?", (language, user_id))
    conn.commit()
    conn.close()