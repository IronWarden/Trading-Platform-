@app.route("/stock/<StockName>")
def stock_detail(StockName):
    # You can render ANY tempate file here, regardless of the route name
    return render_template("/details/index.html")
