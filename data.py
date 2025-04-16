from schedule import IntervalError
import yfinance as yf
import pandas as pd
import redis
import time
import sqlite3

r = redis.Redis(host="localhost", port=6379, db=0)


def fetch_stock(tickers):
    data = yf.download(tickers, period="1d", interval="5m")
    return data


if __name__ == "__main__":
    with sqlite3.connect("./instance/flaskr.sqlite") as conn:
    stock_tickers = []
        db = conn.cursor()
        stocks = db.execute("SELECT Symbol FROM Stocks")
        stock_tickers = [row[0] for row in stocks.fetchall()]

    df = fetch_stock(stock_tickers)
    df.to_csv("data.csv")
