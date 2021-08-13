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

    def strategy(self, index=int):

        if self.indicator.data_array[index] > self.ema_12p.real[index]:

            if self.indicator.data_array[index] > self.bands_1dev.upperband[index]:

                if self.indicator.data_array[index] > self.bands_2dev.upperband[index]:

                    if self.rsi.real[index] > 70:

                        if self.macd.hist[index] > self.macd.hist[index-1]:

                            if self.indicator.data_array[-1] > self.indicator.candles[1][3]:
                                self.order.is_raising = True

                            else:
                                self.order.is_top = True

                        else:
                            self.order.is_top = True

                    else:
                        self.order.is_raising = True

                else:

                    if self.macd.hist[index] > self.macd.hist[index-1]:
                        self.order.is_raising = True

                    else:
                        if self.indicator.data_array[index] >= self.indicator.candles[0][2]:
                            self.order.is_raising = True

                        else:
                            self.order.is_top = True

            else:

                if self.macd.hist[index] > self.macd.hist[index-1]:
                    self.order.is_raising = True

                else:
                    self.order.is_falling = True
        else:

            if self.indicator.data_array[index] > self.bands_1dev.lowerband[index]:

                if self.macd.hist[index] > self.macd.hist[index-1]:
                    self.order.is_raising = True

                else:
                    self.order.is_falling = True
            else:

                if self.indicator.data_array[index] > self.bands_2dev.lowerband[index]:

                    if self.macd.hist[index] > self.macd.hist[index-1]:

                        if self.rsi.real[index] < 40:
                            self.order.is_bottom = True

                        else:
                            self.order.is_raising = True

                    else:

                        if 0.0 > self.macd.macd[-1]:
                            self.order.is_bottom = True

                        else:
                            self.order.is_falling = True

                else:

                    if self.indicator.data_array[index] > self.indicator.candles[0][3]:
                        self.order.is_bottom = True

                    else:
                        self.order.is_falling = True








