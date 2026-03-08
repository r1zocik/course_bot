import urllib.request
import json
import time
import os

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from webdriver_manager.chrome import ChromeDriverManager
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False


def get_chrome_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")

    # На Render chromium стоит по этому пути
    chromium_path = "/usr/bin/chromium"
    if os.path.exists(chromium_path):
        options.binary_location = chromium_path
        service = Service("/usr/bin/chromedriver")
    else:
        service = Service(ChromeDriverManager().install())

    return webdriver.Chrome(service=service, options=options)


def get_cbu_rates() -> dict:
    """Fetch official CBU rates from cbu.uz JSON API."""
    try:
        url = "https://cbu.uz/oz/arkhiv-kursov-valyut/json/"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())

        rates = {"UZS": 1.0}
        for item in data:
            code = item.get("Ccy", "")
            rate = float(item.get("Rate", 0))
            if code in ("USD", "RUB", "EUR"):
                rates[code] = rate
        return rates
    except Exception as e:
        print(f"CBU rate fetch error: {e}")
        return {"UZS": 1.0, "USD": 12179.0, "RUB": 156.73, "EUR": 14139.0}


def get_rates() -> dict:
    return get_cbu_rates()


BANK_URLS = {
    "Kapitalbank":    "https://themoney.uz/banks/kapital-bank/",
    "Ipoteka Bank":   "https://themoney.uz/banks/ipoteka-bank/",
    "Hamkorbank":     "https://themoney.uz/banks/hamkorbank/",
    "Agrobank":       "https://themoney.uz/banks/agro-bank/",
    "NBU (Natsbank)": "https://themoney.uz/banks/natsionalnyj-bank-uzbekistana/",
}


def scrape_bank_rates_selenium(bank_name: str) -> dict:
    """
    Scrape real buy/sell rates from themoney.uz using Selenium.
    Returns: {"USD": {"buy": 12130, "sell": 12210}, "RUB": {"buy": 155, "sell": 158}}
    """
    if not SELENIUM_AVAILABLE:
        print("Selenium not installed")
        return {}

    url = BANK_URLS.get(bank_name)
    if not url:
        return {}

    driver = None
    try:
        driver = get_chrome_driver()
        driver.get(url)

        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "table"))
        )
        time.sleep(2)

        result = {}
        rows = driver.find_elements(By.CSS_SELECTOR, "table tr")

        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) >= 3:
                currency_cell = cells[0].text.strip().upper()
                for cur in ["USD", "RUB"]:
                    if cur in currency_cell:
                        try:
                            buy_text = cells[1].text.strip().replace(" ", "").replace(",", ".")
                            sell_text = cells[2].text.strip().replace(" ", "").replace(",", ".")
                            buy = float(buy_text)
                            sell = float(sell_text)
                            if buy > 10 and sell > 10:
                                result[cur] = {"buy": buy, "sell": sell}
                        except Exception:
                            pass

        return result

    except Exception as e:
        print(f"Selenium scrape error for {bank_name}: {e}")
        return {}
    finally:
        if driver:
            driver.quit()


def get_bank_rates(bank_name: str):
    """
    Returns (bank_rates_dict, cbu_rates_dict, full_info_dict).
    Uses Selenium to get real rates, falls back to CBU + spread.
    """
    cbu = get_cbu_rates()
    web_rates = scrape_bank_rates_selenium(bank_name)

    fallback_spreads = {
        "Kapitalbank":    {"USD": (-50, +30),  "RUB": (-0.6, +0.5)},
        "Ipoteka Bank":   {"USD": (-65, +26),  "RUB": (-0.7, +0.5)},
        "Hamkorbank":     {"USD": (-59, +51),  "RUB": (-0.8, +0.6)},
        "Agrobank":       {"USD": (-49, +31),  "RUB": (-0.5, +0.4)},
        "NBU (Natsbank)": {"USD": (-50, +31),  "RUB": (-0.6, +0.5)},
    }

    bank_rates = {"UZS": 1.0}
    full_info = {}

    for cur in ["USD", "RUB"]:
        if cur in web_rates:
            bank_rates[cur] = web_rates[cur]["sell"]
            full_info[cur] = {**web_rates[cur], "source": "themoney.uz ✅"}
        else:
            spreads = fallback_spreads.get(bank_name, {"USD": (-50, +30), "RUB": (-0.6, +0.5)})
            buy_off, sell_off = spreads.get(cur, (-50, +30))
            cbu_r = cbu.get(cur, 1)
            buy = round(cbu_r + buy_off, 2)
            sell = round(cbu_r + sell_off, 2)
            bank_rates[cur] = sell
            full_info[cur] = {"buy": buy, "sell": sell, "source": "расчётный ⚠️"}

    return bank_rates, cbu, full_info


def convert(amount: float, from_currency: str, to_currency: str, rates: dict) -> float:
    if from_currency == to_currency:
        return amount
    if from_currency == "UZS":
        amount_in_uzs = amount
    else:
        amount_in_uzs = amount * rates.get(from_currency, 1)
    if to_currency == "UZS":
        return amount_in_uzs
    else:
        return amount_in_uzs / rates.get(to_currency, 1)


def format_number(n: float) -> str:
    if n >= 1000:
        return f"{n:,.2f}".replace(",", " ")
    return f"{n:.4f}".rstrip("0").rstrip(".")