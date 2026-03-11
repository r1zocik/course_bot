import os

TOKEN = os.environ.get("TOKEN", "")

# Supported currencies
CURRENCIES = ["UZS", "RUB", "USD"]

CURRENCY_NAMES = {
    "UZS": "🇺🇿 Узбекский сум",
    "RUB": "🇷🇺 Российский рубль",
    "USD": "🇺🇸 Доллар США",
}

# Banks of Uzbekistan
BANKS = {
    "Kapitalbank": "kapitalbank",
    "Ipoteka Bank": "ipotekabank",
    "Hamkorbank": "hamkorbank",
    "Agrobank": "agrobank",
    "NBU (Natsbank)": "nbu",
}
