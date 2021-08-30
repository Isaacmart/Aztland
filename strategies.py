from indicators import Indicator
from indicators import MACD
from indicators import BB
from indicators import VolSMA
from indicators import RSI
from indicators import EMA
from order import Order


class Strategy:

    def __init__(self, indicator=Indicator(), macd=MACD(), bands_1dev=BB(), bands_2dev=BB(), vol_sma=VolSMA(), rsi=RSI(), ema=EMA(), order=Order()):
        self.order = order
        self.indicator = indicator
        self.macd = macd
        self.bands_1dev = bands_1dev
        self.bands_2dev = bands_2dev
        self.volsma = vol_sma
        self.rsi = rsi
        self.ema_12p = ema
        self.index = 0
        self.error = None

    def set_index(self, new_index):
        if self.index == 0:
            self.index = new_index

        else:
            raise Exception('Exception at', new_index)

    def strategy(self, index=int):

        if self.indicator.close_array[index] > self.ema_12p.real[index]:

            if self.indicator.close_array[index] > self.bands_1dev.upperband[index]:

                if self.indicator.close_array[index] > self.bands_2dev.upperband[index]:

                    if self.rsi.real[index] > 70:

                        if self.macd.hist[index] > self.macd.hist[index-1]:

                            if self.indicator.close_array[-1] > self.indicator.candles[1][3]:
                                self.order.is_raising = True
                                self.set_index(1)

                            else:
                                self.order.is_top = True
                                self.set_index(2)

                        else:
                            self.order.is_top = True
                            self.set_index(3)

                    else:
                        self.order.is_raising = True
                        self.set_index(4)
                else:

                    if self.macd.hist[index] > self.macd.hist[index-1]:
                        self.order.is_raising = True
                        self.set_index(5)

                    else:
                        if self.indicator.close_array[index] >= self.indicator.candles[0][2]:
                            self.order.is_raising = True
                            self.set_index(6)

                        else:
                            self.order.is_top = True
                            self.set_index(7)

            else:

                if self.macd.hist[index] > self.macd.hist[index-1]:
                    self.order.is_raising = True
                    self.set_index(8)

                else:
                    self.order.is_falling = True
                    self.set_index(9)
        else:

            if self.indicator.close_array[index] > self.bands_1dev.lowerband[index]:

                if self.macd.hist[index] > self.macd.hist[index-1]:
                    self.order.is_raising = True
                    self.set_index(10)

                else:
                    self.order.is_falling = True
                    self.set_index(11)
            else:

                if self.indicator.close_array[index] > self.bands_2dev.lowerband[index]:

                    if self.macd.hist[index] > self.macd.hist[index-1]:

                        if self.rsi.real[index] < 40:
                            self.order.is_bottom = True
                            self.set_index(12)

                        else:
                            self.order.is_raising = True
                            self.set_index(13)

                    else:

                        if 0.0 > self.macd.macd[-1]:
                            self.order.is_bottom = True
                            self.set_index(14)

                        else:
                            self.order.is_falling = True
                            self.set_index(15)

                else:

                    if self.indicator.close_array[index] > self.indicator.candles[0][3]:
                        self.order.is_bottom = True
                        self.set_index(16)

                    else:
                        self.order.is_falling = True
                        self.set_index(17)










