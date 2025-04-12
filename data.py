import yfinance as yf
import pandas as pd
import redis 
import time 
import sqlite3

r = redis.Redis(host='localhost', port=6379, db=0)

def fetch_stock():
    
    return stock

if __name__ == "__main__":
    stock_tickers = []
    with sqlite3.connect('/instance/flaskr.sqlite') as conn:
        db = conn.cursor()
        stocks = db.execute("SELECT Symbol FROM Stocks")
        stock_tickers = [row[0] for row in stocks.fetchall()]

    while True:

