

import os
import json
import time
import requests
from datetime import datetime

API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")
BASE_URL = "https://www.alphavantage.co/query"

SYMBOLS = ["AAPL", "MSFT"]
FUNCTION = "TIME_SERIES_DAILY"
LANDING_ZONE = "landing_zone"

MAX_RETRIES = 5
BACKOFF_BASE = 2


def fetch_daily_stock(symbol):
    params = {
        "function": FUNCTION,
        "symbol": symbol,
        "apikey": API_KEY,
        "outputsize": "compact"
    }

    retries = 0
    while retries < MAX_RETRIES:
        response = requests.get(BASE_URL, params=params, timeout=15)

        if response.status_code == 200:
            data = response.json()

            if "Note" in data:
                wait = BACKOFF_BASE ** retries
                print(f"Rate limit hit. Waiting {wait}s...")
                time.sleep(wait)
                retries += 1
            else:
                return data

        else:
            wait = BACKOFF_BASE ** retries
            time.sleep(wait)
            retries += 1

    raise Exception(f"Failed to fetch data for {symbol}")


def save_raw_json(symbol, data):
    os.makedirs(LANDING_ZONE, exist_ok=True)

    today = datetime.utcnow().strftime("%Y%m%d")
    filename = f"daily_stock_{symbol}_{today}.json"
    filepath = os.path.join(LANDING_ZONE, filename)

    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)

    print(f"Saved {filepath}")


if __name__ == "__main__":
    if not API_KEY:
        raise EnvironmentError("ALPHAVANTAGE_API_KEY not set")

    for symbol in SYMBOLS:
        print(f"Ingesting {symbol}...")
        data = fetch_daily_stock(symbol)
        save_raw_json(symbol, data)
        time.sleep(15)  