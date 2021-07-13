import backtrader

cerebro = backtrader.cerebro

cerebro.broker.set_cash(10000)
print("starting portofolio value: %.2f" % cerebro.broker.getValue())

cerebro.run()
