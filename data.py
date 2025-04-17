import yfinance as yf
import pandas as pd
import redis
import time
import sqlite3

r = redis.Redis(host="localhost", port=6379, db=0)


def fetch_stock(tickers):
    data = yf.download(tickers, period="1d", interval="5m")
    return data


def store_redis(stocks_data, stocks_tickers):
    try:
        print("storing data in redis")
        for ticker in stocks_tickers:
            if ticker in stocks_data.columns.levels[0]:
                ticker_data = stocks_data[ticker]
                r.set(f"stock{ticker}", ticker_data.to_json(orient="split"))
                r.set(
                    f"stock{ticker}:last_updated", ticker_data.to_json(orient="split")
                )
    except Exception as e:
        print("failed to store data in redis")


if __name__ == "__main__":
    stock_tickers = []
    with sqlite3.connect("./instance/flaskr.sqlite") as conn:
        db = conn.cursor()
        stocks = db.execute("SELECT Symbol FROM Stocks")
        stock_tickers = [row[0] for row in stocks.fetchall()]

    df = fetch_stock(stock_tickers)
    store_redis(df, stock_tickers)
    df.to_csv("data.csv")
