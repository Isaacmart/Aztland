from indicators import Indicator
from indicators import MACD
from indicators import BB
from indicators import VolSMA
from indicators import RSI
from indicators import EMA
from indicators import ROC
from order import Order


class Strategy:

    index: int
    error: str
    order: Order

    def __init__(self, indicator=Indicator(), macd=MACD(), bands_1dev=BB(), bands_2dev=BB(), vol_sma=VolSMA(), rsi=RSI(), ema=EMA(), roc=ROC(), order=Order()):
        self.order = order
        self.indicator = indicator
        self.macd = macd
        self.bands_1dev = bands_1dev
        self.bands_2dev = bands_2dev
        self.volsma = vol_sma
        self.rsi = rsi
        self.roc = roc
        self.ema_12p = ema
        self.error = ""
        self.index = 0

    def set_index(self, new_index):
        if self.index == 0:
            self.index = new_index

        else:
            raise Exception('Exception at', new_index)

    def reset_order(self):
        self.order.is_top = False
        self.order.is_bottom = False
        self.order.is_raising = False
        self.order.is_falling = False

    def strategy(self, index=-1, beg=0):

        if self.macd.macd[index] <= self.macd.signal[index]:
            if self.macd.macd[index - 1] > self.macd.signal[index - 1]:
                self.order.is_top = True
                self.set_index(1)
        if self.macd.macd[index] >= self.macd.signal[index]:
            if self.macd.macd[index - 1] < self.macd.signal[index - 1]:
                self.order.is_bottom = True
                self.set_index(2)
