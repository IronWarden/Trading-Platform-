from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort
from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint("details", __name__)


@bp.route("/stock/<StockName>")
def stock_detail(StockName):
    # You can render ANY tempate file here, regardless of the route name
    return render_template("/details/index.html")
