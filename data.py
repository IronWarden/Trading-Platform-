import yfinance as yf
import pandas as pd
import redis 
import time 

r = redis.Redis(host='localhost', port=6379, db=0)



if __name__ == "__main__":
    while True:
        tickers = r.get('tickers').decode('utf-8')
        tickers = tickers.split(',')
        for ticker in tickers:
