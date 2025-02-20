from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from flaskr.auth import login_required
from flaskr.db import get_db
import requests
import pandas as pd
import yfinance as yf
bp = Blueprint('dashboard', __name__)


def get_sp500_stocks():
    """Fetch S&P 500 stock symbols from Wikipedia."""
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    tables = pd.read_html(url)
    sp500_table = tables[0]
    symbols = sp500_table['Symbol'].tolist()
    names = sp500_table['Security'].tolist()
    return list(zip(symbols, names))


def write_stocks_to_db(stocks):
    db = get_db()
    db.executemany('INSERT INTO Stocks (Symbol, Name) VALUES (?, ?)', stocks)
    db.commit()

# find stocks from db


def get_stocks_names_from_db():
    db = get_db()
    stocks = db.execute('SELECT Name FROM Stocks')
    stock_names = [row[0] for row in stocks.fetchall()]
    return stock_names

def get_stocks_symbols_from_db():
    db = get_db()
    stocks = db.execute('SELECT Symbol FROM Stocks')
    stock_symbols = [row[0] for row in stocks.fetchall()]
    return stock_symbols

@bp.route('/home')
def index():
    stocks_names = get_stocks_from_db()
    stocks = []
    return render_template('dashboard/index.html')
