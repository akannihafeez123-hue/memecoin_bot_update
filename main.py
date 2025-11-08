import os
import requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("ADMIN_CHAT_ID")

CONTRACTS = {
    "PEPE": "0x6982508145454Ce325dDbE47a25d4ec3d2311933",
    "SHIBA INU": "0x95aD61b0a150d79219dCF64E1E6Cc01f0B64C4cE",
    "DOGECOIN": None
}

def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }
    requests.post(url, data=payload)

def fetch_meme_coins():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "ids": "pepe,shiba-inu,dogecoin",
        "order": "market_cap_desc",
        "per_page": 3,
        "page": 1,
        "price_change_percentage": "24h"
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print("Error fetching data:", e)
        return []

def format_alert(coin):
    name = coin["name"].upper()
    symbol = coin["symbol"].upper()
    contract = CONTRACTS.get(name)
    price = coin["current_price"]
    change = coin.get("price_change_percentage_24h", 0)
    volume = coin.get("total_volume", 0)

    msg = (
        f"🔥 *${symbol}* is trending!\n"
        f"💰 Price: ${price:.6f}\n"
        f"📈 24h Change: {change:.2f}%\n"
        f"📊 Volume: ${volume:,.0f}\n"
    )

    if contract:
        msg += (
            f"📜 Contract: `{contract}`\n"
            f"🛒 [Buy on Uniswap](https://app.uniswap.org/#/swap?outputCurrency={contract})\n"
        )
    else:
        msg += "📜 Native coin — no contract address\n"

    msg += f"🔗 [View on CoinGecko](https://www.coingecko.com/en/coins/{coin['id']})"
    return msg

def main():
    coins = fetch_meme_coins()
    for coin in coins:
        alert = format_alert(coin)
        send_message(alert)

if __name__ == "__main__":
    main()
