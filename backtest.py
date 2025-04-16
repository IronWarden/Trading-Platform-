import numpy as np
import pandas as pd
import sqlite3
import vectorbt as vbt


def fetch_stock(tickers):
    data = yf.download(tickers, period="1mo")
    return data


if __name__ == "__main__":
    stock_tickers = []

    with sqlite3.connect("./instance/flaskr.sqlite") as conn:
        db = conn.cursor()
        stocks = db.execute("SELECT Symbol FROM Stocks")
        stock_tickers = [row[0] for row in stocks.fetchall()]

    print(stock_tickers)
    data = vbt.YFData.download(stock_tickers, start="2010-01-01", end="2023-12-31").get(
        "close"
    )

    # calculate smas
    sma10 = vbt.ma.run(data, window=10)
    sma50 = vbt.ma.run(data, window=50)

    # generate signals
    entries = sma10.ma_crossed_below(sma50)  # buy when 10-day crosses below 50-day
    exits = sma10.ma_crossed_above(sma50)  # sell when 10-day crosses above 50-day

    # run backtest
    portfolio = vbt.portfolio.from_signals(
        data,
        entries=entries,
        exits=exits,
        fees=0.0025,  # 0.25% commission per trade
        freq="d",  # daily frequency
    )

    # print performance metrics
    print(portfolio.stats())

    # plot equity curve
    portfolio.plot().show()

    # plot trades with smas
    fig = data.vbt.plot(trace_kwargs=dict(name="price"))
    sma10.ma.vbt.plot(trace_kwargs=dict(name="10-day sma"), fig=fig)
    sma50.ma.vbt.plot(trace_kwargs=dict(name="50-day sma"), fig=fig)
    portfolio.positions.plot(trace_kwargs=dict(visible=false), fig=fig)
    fig.show()
