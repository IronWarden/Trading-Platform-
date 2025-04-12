from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort
from flaskr.auth import login_required
from flaskr.db import get_db
import pandas as pd
import yfinance as yf

bp = Blueprint("dashboard", __name__)


class stock:
    def __init__(self, symbol, name, description, price=None):
        self.symbol = symbol
        self.name = name
        self.price = price
        self.description = description


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
    stock_tickers = [row[0] for row in stocks.fetchall()]
    return stock_tickers


def update_stock_description(description, stock_ticker):
    db = get_db()
    db.execute(
        "UPDATE Stocks SET Description = ? WHERE Symbol = ?",
        (description, stock_ticker),
    )
    db.commit()


def alter_stocks(stock_tickers):
    for ticker in stock_tickers:
        stock = yf.Ticker(ticker)
        description = str(stock.info.get("longBusinessSummary", ""))
        if description:
            update_stock_description(description, ticker)


def get_stock_descriptions_from_db():
    db = get_db()
    stocks = db.execute("SELECT Description FROM Stocks")
    descriptions = [row[0] for row in stocks.fetchall()]
    return descriptions


@bp.route("/home")
def index():
    stock_names = get_stocks_names_from_db()
    stock_ticker = get_stocks_symbols_from_db()
    stock_descriptions = get_stock_descriptions_from_db()
    stocks = [
        stock(symbol, name, description)
        for symbol, name, description in zip(
            stock_ticker, stock_names, stock_descriptions
        )
    ]

    return render_template("dashboard/index.html", stocks=stocks)
