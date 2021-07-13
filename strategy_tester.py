import backtrader

cerebro = backtrader.Cerebro()

cerebro.broker.set_cash(10000)
print("starting portofolio value: %.2f" % cerebro.broker.get_value())

cerebro.run()
