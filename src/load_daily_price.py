import json
import psycopg2
from datetime import datetime


conn = psycopg2.connect(
    dbname="stocks",
    user="user",
    password="password",
    host="localhost",
    port="5432"
)
cur = conn.cursor()


with open("landing_zone/daily_stock_AAPL_20251216.json") as f:
    data = json.load(f)

symbol = data["Meta Data"]["2. Symbol"]
time_series = data["Time Series (Daily)"]


cur.execute("""
    INSERT INTO exchange (exchange_name, timezone)
    VALUES (%s, %s)
    ON CONFLICT DO NOTHING
""", ("NASDAQ", "US/Eastern"))


cur.execute("""
    INSERT INTO stock (symbol, exchange_id)
    SELECT %s, exchange_id FROM exchange WHERE exchange_name = %s
    ON CONFLICT (symbol) DO NOTHING
""", (symbol, "NASDAQ"))


cur.execute("SELECT stock_id FROM stock WHERE symbol = %s", (symbol,))
stock_id = cur.fetchone()[0]

for trade_date, prices in time_series.items():
    cur.execute("""
        INSERT INTO daily_price (
            stock_id, trade_date, open_price,
            high_price, low_price, close_price, volume
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (stock_id, trade_date)
        DO UPDATE SET
            open_price = EXCLUDED.open_price,
            high_price = EXCLUDED.high_price,
            low_price = EXCLUDED.low_price,
            close_price = EXCLUDED.close_price,
            volume = EXCLUDED.volume
    """, (
        stock_id,
        datetime.strptime(trade_date, "%Y-%m-%d").date(),
        float(prices["1. open"]),
        float(prices["2. high"]),
        float(prices["3. low"]),
        float(prices["4. close"]),
        int(prices["5. volume"])
    ))

conn.commit()
cur.close()
conn.close()