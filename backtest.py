from datetime import datetime
import backtrader as bt
import yfinance as yf


class AllCashSmaStrategy(bt.Strategy):
    params = (
        ("fast_period", 10),
        ("slow_period", 30),
        ("trail_percent", 3.0),
    )

    def __init__(self):
        self.fast_sma = bt.ind.SMA(period=self.p.fast_period)
        self.slow_sma = bt.ind.SMA(period=self.p.slow_period)
        self.crossover = bt.ind.CrossOver(self.fast_sma, self.slow_sma)
        self.highest_high = None
        self.order = None

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    f"BUY EXECUTED, Price: {order.executed.price:.2f}, Cost: {order.executed.value:.2f}, Comm: {order.executed.comm:.2f}"
                )
            elif order.issell():
                self.log(
                    f"SELL EXECUTED, Price: {order.executed.price:.2f}, Cost: {order.executed.value:.2f}, Comm: {order.executed.comm:.2f}"
                )
            self.bar_executed = len(self)
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log("Order Canceled/Margin/Rejected")

        self.order = None

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print(f"{dt.isoformat()}, {txt}")

    def next(self):
        if self.order:
            return

        if not self.position:
            if self.crossover > 0:
                cash = self.broker.getcash()
                price = self.data.close[0]
                size = int(cash / price)

                if size > 0:
                    self.log(f"BUY CREATE, Size: {size}, Price: {price:.2f}")
                    self.order = self.buy(size=size)
                    self.highest_high = self.data.high[0]
        else:
            if self.data.high[0] > self.highest_high:
                self.highest_high = self.data.high[0]

            stop_price = self.highest_high * (1 - self.p.trail_percent / 100)
            if self.crossover < 0 or self.data.close[0] < stop_price:
                self.log(f"SELL CREATE, Price: {self.data.close[0]:.2f}")
                self.order = self.close()


# Initialize Cerebro properly
cerebro = bt.Cerebro()
cerebro.broker.setcash(10000.0)
cerebro.broker.setcommission(commission=0.000)

# Data handling with explicit column names
data = yf.download("AAPL", "2015-01-01", "2025-01-01", auto_adjust=False)
data = data[["Open", "High", "Low", "Close", "Volume"]]
data.columns = ["open", "high", "low", "close", "volume"]

datafeed = bt.feeds.PandasData(
    dataname=data,
    datetime=None,
    open=0,
    high=1,
    low=2,
    close=3,
    volume=4,
    openinterest=-1,
)

cerebro.adddata(datafeed)
cerebro.addstrategy(AllCashSmaStrategy)

# Add analyzers
cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name="sharpe")
cerebro.addanalyzer(bt.analyzers.Returns, _name="returns")
cerebro.addanalyzer(bt.analyzers.DrawDown, _name="drawdown")

print(f"Starting Portfolio Value: {cerebro.broker.getvalue():.2f}")

# Run strategy
results = cerebro.run()

# Print results
print(f"Final Portfolio Value: {cerebro.broker.getvalue():.2f}")
strat = results[0]
print("Sharpe Ratio:", strat.analyzers.sharpe.get_analysis()["sharperatio"])
print("Annual Return:", strat.analyzers.returns.get_analysis()["rnorm100"])
print("Max Drawdown:", strat.analyzers.drawdown.get_analysis()["max"]["drawdown"])

# Plot with proper initialization
cerebro.plot(iplot=False, volume=False)
