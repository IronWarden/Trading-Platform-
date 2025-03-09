from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort
from flaskr.SECRETS import API_KEY
from flaskr.auth import login_required
from flaskr.db import get_db
import pandas as pd
import yfinance as yf
import finnhub

bp = Blueprint("dashboard", __name__)


class stock:
    def __init__(self, symbol, name, price=None):
        self.symbol = symbol
        self.name = name
        self.price = price


def get_sp500_stocks():
    """Fetch S&P 500 stock symbols from Wikipedia."""
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    tables = pd.read_html(url)
    sp500_table = tables[0]
    symbols = sp500_table["Symbol"].tolist()
    names = sp500_table["Security"].tolist()
    return list(zip(symbols, names))


def write_stocks_to_db(stocks):
    db = get_db()
    db.executemany("INSERT INTO Stocks (Symbol, Name) VALUES (?, ?)", stocks)
    db.commit()


# find stocks from db
def get_stocks_names_from_db():
    db = get_db()
    stocks = db.execute("SELECT Name FROM Stocks")
    stock_names = [row[0] for row in stocks.fetchall()]
    return stock_names


def get_stocks_symbols_from_db():
    db = get_db()
    stocks = db.execute("SELECT Symbol FROM Stocks")
    stock_symbols = [row[0] for row in stocks.fetchall()]
    return stock_symbols


def update_stock_description(description, stock_ticker):
    db = get_db()
    db.execute(
        "UPDATE Stocks SET Description = ? WHERE Symbol = ?",
        (description, stock_ticker),
    )


def alter_stocks(stock_symbols):
    for ticker in stock_symbols:
        stock = yf.Ticker(ticker)
        description = str(stock.info.get("longBusinessSummary", ""))
        if description:
            update_stock_description(description, ticker)
            print(f"successfully updated {ticker}")


@bp.route("/home")
def index():
    stock_names = get_stocks_names_from_db()
    stocks_symbols = get_stocks_symbols_from_db()
    alter_stocks(stocks_symbols)
    stocks = [
        stock(symbol, name, price=1000)
        for symbol, name in zip(stocks_symbols, stock_names)
    ]

    return render_template("dashboard/index.html", stocks=stocks)
