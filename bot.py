import requests
import time
import os

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

LEVELS = [float(x) for x in os.getenv("LEVELS", "0.20").split(",")]

CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "5"))

def send_msg(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.get(url, params={"chat_id": CHAT_ID, "text": text})

def get_price():
    url = "https://api.dex-trade.com/v1/public/ticker?pair=TXCUSDT"
    r = requests.get(url, timeout=10)
    data = r.json()
    return float(data["data"]["last"])

last_price = get_price()

while True:
    price = get_price()

    for level in LEVELS:
        if last_price < level <= price:
            send_msg(f"🚀 Пробой вверх уровня {level}\nЦена: {price}")

        if last_price > level >= price:
            send_msg(f"📉 Пробой вниз уровня {level}\nЦена: {price}")

    last_price = price
    time.sleep(CHECK_INTERVAL)
