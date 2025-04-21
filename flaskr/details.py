from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort
from flaskr.auth import login_required
from flaskr.db import get_db
import pandas as pd

bp = Blueprint("details", __name__)


@bp.route("/stock/<StockName>")
def stock_detail(StockName):
    df = pd.read_parquet("./data.parquet", engine="pyarrow")

    # You can render ANY tempate file here, regardless of the route name
    return render_template("/details/index.html")
