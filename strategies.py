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

    def strategy(self, index=int, beg=0):

        #Check whether price is over the 12 period EMA line
        if self.indicator.close_array[index] > self.ema_12p.real[index]:

            #Checks whether price is over the 1 deviation Bollinger upper band
            if self.indicator.close_array[index] > self.bands_1dev.upperband[index]:

                #Checks whether price is over the 2 deviation Bollinger upper band
                if self.indicator.close_array[index] > self.bands_2dev.upperband[index]:

                    #Checks whether the RSI is over 70
                    if self.rsi.real[index] > 70:

                        #Checks whether the MACD histogram is over the previous value
                        if self.macd.hist[index] > self.macd.hist[index-1]:

                            #Checks whether the current price is over the opening price for that candlestick
                            #If is_raising is True, the token price is raising
                            if self.indicator.close_array[index] > self.indicator.candles[beg][3]:
                                self.order.is_raising = True
                                self.set_index(1)

                            #If the last if statement is False, the token is at a top price
                            else:
                                self.order.is_top = True
                                self.set_index(2)

                        #If this if statement is False, the token is at a top price
                        else:
                            self.order.is_top = True
                            self.set_index(3)

                    #If this if-statement is False, the token is raising
                    else:
                        self.order.is_raising = True
                        self.set_index(4)

                #If the price is not over the 2 deviation Bollinger upper band, more analysis has to been done
                else:

                    #If the last MACD histogram value is over the previous value, the token is raising
                    if self.macd.hist[index] > self.macd.hist[index-1]:
                        self.order.is_raising = True
                        self.set_index(5)

                    #In case that is False
                    else:

                        #If the price is over the opening price, the token is raising
                        if self.indicator.close_array[index] >= self.indicator.candles[beg][2]:
                            self.order.is_raising = True
                            self.set_index(6)

                        #If the last statement is False, the token is at a top
                        else:
                            self.order.is_top = True
                            self.set_index(7)

            #If price is not over the 1 deviation Bollinger upper band, more analysis needs to be done
            else:

                #If the MACD histogram value is over the previous value, the token price is raising
                if self.macd.hist[index] > self.macd.hist[index-1]:
                    self.order.is_raising = True
                    self.set_index(8)

                #If the last if-stament is False, the token is falling
                else:
                    self.order.is_falling = True
                    self.set_index(9)

        #If price is not over the 12 period EMA line, more analysis is conducted
        else:

            #If the price is over the 1 deviation Bollinger lower band
            if self.indicator.close_array[index] > self.bands_1dev.lowerband[index]:

                #If the last MACD histogram value is over the previous one, price is raising
                if self.macd.hist[index] > self.macd.hist[index-1]:
                    self.order.is_raising = True
                    self.set_index(10)

                #If not, price is falling
                else:
                    self.order.is_falling = True
                    self.set_index(11)

            #If the price is not over 1 deviation Bollinger lower
            else:

                #If price is over the 2 deviation Bollinger lower band
                if self.indicator.close_array[index] > self.bands_2dev.lowerband[index]:

                    #If the last MACD histogram
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

                    if self.indicator.close_array[index] > self.indicator.candles[beg][3]:
                        self.order.is_bottom = True
                        self.set_index(16)

                    else:
                        self.order.is_falling = True
                        self.set_index(17)










