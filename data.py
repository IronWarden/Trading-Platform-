import yfinance as yf
import pandas as pd
import time
import sqlite3
import json
from pathlib import Path


def fetch_stock(tickers):
    return yf.download(tickers, period="max", interval="1d")


def update_stock_data(df):
    temp_path = "temp.parquet"
    df.to_parquet(temp_path, engine="pyarrow")

    # atomic rename to ensure user gets correct data
    Path(temp_path).replace("data.parquet")


if __name__ == "__main__":
    stock_tickers = []
    with sqlite3.connect("./instance/flaskr.sqlite") as conn:
        db = conn.cursor()
        stocks = db.execute("SELECT Symbol FROM Stocks")
        stock_tickers = [row[0] for row in stocks.fetchall()]

    df = fetch_stock(stock_tickers)
    update_stock_data(df)
