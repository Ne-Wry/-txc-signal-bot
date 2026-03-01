import requests
import time
import os

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
LEVEL = float(os.getenv("LEVEL", "0.20"))
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

    if last_price < LEVEL <= price:
        send_msg(f"🚀 Пробой вверх TXC/USDT уровня {LEVEL}\nЦена: {price}")

    if last_price > LEVEL >= price:
        send_msg(f"📉 Пробой вниз TXC/USDT уровня {LEVEL}\nЦена: {price}")

    last_price = price
    time.sleep(CHECK_INTERVAL)
