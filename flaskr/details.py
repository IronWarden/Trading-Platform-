from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort
from flaskr.auth import login_required
from flaskr.db import get_db
import pandas as pd
import plotly.graph_objects as go


bp = Blueprint("details", __name__)


def create_plot(df, ticker):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df["Close"][ticker], name="Close"))
    fig.update_layout(
        title=f"{ticker} Stock Price",
        xaxis_title="Date",
        yaxis_title="Price",
        template="plotly_dark",
    )
    return fig.to_html()


@bp.route("/stock/<StockName>")
def stock_detail(StockName):
    df = pd.read_parquet("./data.parquet", engine="pyarrow")

    chart = create_plot(df, StockName)
    # You can render ANY tempate file here, regardless of the route name
    return render_template("/details/index.html", chart=chart, ticker=StockName)
