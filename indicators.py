import numpy
import talib
from cbpro import PublicClient
from app_methods import *


class Indicator:

    '''
    Index 4 will create a list with close price values
    Gets a initialized PublicClient as parameter
    '''
    def __init__(self, client=PublicClient, index=4, weight=True):
        self.new_client = client
        self.candles = []
        self.data_array = []
        self.np_array = []
        self.index = index
        self.weight = weight

    def set_candles(self, product, callback, begin, granularity):
        self.candles = self.new_client.get_product_historic_rates(product_id=product,
                                                                  start=callback, end=begin, granularity=granularity)

        return self.candles

    def get_data_set(self):

        for candle in self.candles:
            self.data_array.append(candle[self.index])

        return self.data_array

    def reverse_data(self):

        self.data_array.reverse()
        return self.data_array

    def get_np_array(self):

        self.np_array = numpy.array(self.data_array)

        return self.np_array


class MACD(Indicator):

    def __init__(self, client=PublicClient, fastperiod=12, slowperiod=26, signalperiod=9):
        super(MACD, self).__init__(client=client)
        self.macd = []
        self.hist = []
        self.signal = []
        self.fast_period = fastperiod
        self.slow_period = slowperiod
        self.signal_period = signalperiod

    def get_MACD(self):

        self.macd, self.signal, self.hist = talib.MACD(real=self.np_array, fastperiod=self.fast_period,
                                                          slowperiod=self.slow_period, signalperiod=self.signal_period)


class BB(Indicator):

    def __init__(self, client=PublicClient, timeperiod=5, ndbevup=2, nbdevdn=2, matype=0, index=4, weight=False):
        super(BB, self).__init__(client=client, index=index, weight=weight)
        self.upperband = []
        self.middleband = []
        self.lowerband = []
        self.timeperiod = timeperiod
        self.ndbevup = ndbevup
        self.nbdevdn = nbdevdn
        self.matye = matype

    def get_BB(self):

        self.upperband, self.middleband, self.lowerband = talib.BBANDS(real=self.np_array, timeperiod=self.timeperiod,
                                                                       nbdevup=self.ndbevup, nbdevdn=self.nbdevdn,
                                                                       matype=self.matye)


class VolSMA(Indicator):

    '''index = 5 will create an array with volume values'''
    def __init__(self, client=PublicClient, timeperiod=30, index=5, weight=False):
        super(VolSMA, self).__init__(client=client, index=index, weight=weight)
        self.timeperiod = timeperiod
        self.real = []

    def get_volume(self):

        self.real = talib.SMA(real=self.np_array, timeperiod=self.timeperiod)
        return self.real


class RSI(Indicator):

    def __init__(self, client=PublicClient, timeperiod=14, index=4, weight=False):
        super(RSI, self).__init__(client=client, index=index, weight=weight)
        self.timperiod = timeperiod
        self.real = []

    def get_RSI(self):

        self.real = talib.RSI(real=self.np_array, timeperiod=self.timperiod)


class EMA(Indicator):

    def __init__(self, client=PublicClient, time_period=12, index=4):
        super(EMA, self).__init__(client=client, index=index)
        self.timeperiod = time_period
        self.real = []

    def get_EMA(self):

        self.real = talib.EMA(real=self.np_array, timeperiod=self.timeperiod)


'''
new_client = PublicClient()
volume = VOLSMA(client=new_client, timeperiod=20)
volume.set_candles(product='ETH-USD', callback=get_time(27976), begin=get_time(0), granularity=300)
volume.get_data_set()
volume.reverse_data()
volume.get_volume()
print(volume.real)

bands = BB(client=new_client)
bands.set_candles(product='ETH-USD', callback=get_time(27976), begin=get_time(0), granularity=300)
bands.get_data_set()
bands.reverse_data()
bands.get_BB()
print(bands.upperband)

m15_macd = MACD(client=new_client)
m15_macd.set_candles(product='ETH-USD', callback=get_time(27976), begin=get_time(0), granularity=300)
m15_macd.get_data_set()
m15_macd.reverse_data()
m15_macd.get_MACD()
print(m15_macd.hist[-1])
'''



















