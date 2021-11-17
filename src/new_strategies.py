from strategies import Strategy
from indicators import Indicator
from indicators import MACD
from indicators import RSI
from indicators import BB
from indicators import ROC
from order import Order


class MACDStrategy(Strategy):

    def __init__(self, macd=MACD(), order=Order()):
        super(MACDStrategy, self).__init__(macd=macd, order=order)

    def strategy(self, index=-1, beg=0):
        if self.macd.macd[index] <= self.macd.signal[index]:
            if self.macd.macd[index-1] > self.macd.signal[index-1]:
                self.order.is_top = True
                self.set_index(1)
        if self.macd.macd[index] >= self.macd.signal[index]:
            if self.macd.macd[index-1] < self.macd.signal[index-1]:
                self.order.is_bottom = True
                self.set_index(2)


class RSISTrategy(Strategy):

    def __init__(self, rsi=RSI(), order=Order()):
        super(RSISTrategy, self).__init__(rsi=rsi, order=order)

    def strategy(self, index=-1, beg=0):
        if self.rsi.real[index] >= 70.0:
            self.order.is_top = True
            self.set_index(1)

        elif self.rsi.real[index] <= 30.0:
            self.order.is_bottom = True
            self.set_index(2)


class Bollinger(Strategy):

    def __init__(self, indicator=Indicator(), bol=BB(), order=Order()):
        super(Bollinger, self).__init__(indicator=indicator, bands_2dev=bol, order=order)

    def strategy(self, index=-1, beg=0):
        if self.indicator.close_array[index] <= self.bands_2dev.lowerband[index]:
            self.order.is_bottom = True
            self.set_index(1)
        elif self.indicator.close_array[index] >= self.bands_2dev.upperband[index]:
            self.order.is_top = True
            self.set_index(2)


class RateOfChange(Strategy):

    def __init__(self, roc=ROC(), order=Order()):
        super(RateOfChange, self).__init__(roc=roc, order=order)

    def strategy(self, index=-1, beg=0):
        if self.roc.real[index] <= -1.0:
            self.order.is_bottom = True
            self.set_index(1)
        elif self.roc.real[index] >= 1.0:
            self.order.is_top = True
            self.set_index(2)
