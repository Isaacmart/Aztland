import backtrader

cerebro = backtrader.Cerebro()

data = backtrader.feeds.GenericCSVData(
    dataname="data/CB_stocks_NKNUSD.csv",
    nullvalue=0.0,
    dtformat=2,
    openinterest=-1
)

cerebro.adddata(data)


