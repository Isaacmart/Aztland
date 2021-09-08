import numpy
import talib
from cbpro import PublicClient


class Indicator:
    """
    Base class for any indicator.
    Coinbase returns data in the following way: [1415398768, 0.32, 4.2, 0.35, 4.2, 12.3],
    indicators work with close prices as default, therefore we append data from index 4
    If the indicator is weighted, certain amount of elements back are needed,
    weight = True will get that many elements automatically
    """

    def __init__(self, index=4, weight=True):
        """
        Creates an instance of the Indicator class

        Args:
             index (int): type of price to work with, close price is default
             weight (bool): If
        """
        self.new_client = PublicClient(timeout=45)
        self.candles = []
        self.close_array = []
        self.date_array = []
        self.np_array = []
        self.index = index
        self.weight = weight

    def initiate_client(self, client=PublicClient):
        """
        Passes an instance class needed for getting indicators

        Args:
            client (PublicClient): Instance of PublicClient
        """
        self.__doc__ += PublicClient.__doc__
        self.new_client = client

    def set_candles(self, product, callback, begin, granularity):
        """
        Makes requests to the Coinbase API for Historic rates

        Args:
            product (str): A valid Coinbase product
            callback (int):  Number of seconds to go back from begin
            begin (int): Last second to get rates from
            granularity (int): Number of seconds
        """
        self.candles = self.new_client.get_product_historic_rates(product_id=product, start=callback, end=begin, granularity=granularity)

        return self.candles

    def get_data_set(self):
        """
        Gets a data set in a list

        :return: A list with the closing prices of a product
        """

        for candle in self.candles:
            self.close_array.append(float(candle[self.index]))

        return self.close_array

    def reverse_data(self):
        """
        Reverses the list containing the closing price.
        Coinbase yields the latest data first; however, to
        get accurate numbers, the data passed to the

        :return: List with closing prices reversed
        """

        self.close_array.reverse()
        return self.close_array

    def get_dates(self):
        """
        Puts of the dates in a list an reverses it
        in the same method. That is because when we
        testing strategies sometimes we wanna see when
        it happened and we this method we just have to
        reference the same index as the one in the
        closing prices list

        :return: Reversed list of dates in Unix form
        """

        p = 0
        while p < len(self.candles):
            self.date_array.append(self.candles[p][0])
            p = p + 1

        self.date_array.reverse()

        return self.date_array

    def get_np_array(self):
        """
        Ta-Lib takes data in a numpy array, this
        method coverts a regular list into a numpy
        array

        :return: Numpy array of closing prices
        """

        self.np_array = numpy.array(self.close_array)
        return self.np_array


class MACD(Indicator):
    """
    Implementation of the MACD indicator, inherits
    Indicator and
    """

    def __init__(self, fastperiod=12, slowperiod=26, signalperiod=9, index=4, weight=True):
        super(MACD, self).__init__(index=index, weight=True)
        self.macd = []
        self.hist = []
        self.signal = []
        self.fast_period = fastperiod
        self.slow_period = slowperiod
        self.signal_period = signalperiod

    def get_MACD(self):

        self.macd, self.signal, self.hist = talib.MACD(real=self.np_array, fastperiod=self.fast_period, slowperiod=self.slow_period, signalperiod=self.signal_period)
        return self.macd


class BB(Indicator):

    def __init__(self, timeperiod=5, ndbevup=2, nbdevdn=2, matype=0, index=4, weight=False):
        super(BB, self).__init__(index=index, weight=weight)
        self.upperband = []
        self.middleband = []
        self.lowerband = []
        self.timeperiod = timeperiod
        self.ndbevup = ndbevup
        self.nbdevdn = nbdevdn
        self.matye = matype

    def get_BB(self):

        self.upperband, self.middleband, self.lowerband = talib.BBANDS(real=self.np_array, timeperiod=self.timeperiod, nbdevup=self.ndbevup, nbdevdn=self.nbdevdn, matype=self.matye)
        return self.upperband


class VolSMA(Indicator):

    '''index = 5 will create an array with volume values'''
    def __init__(self, timeperiod=30, index=5, weight=False):
        super(VolSMA, self).__init__(index=index, weight=weight)
        self.timeperiod = timeperiod
        self.real = []

    def get_volume(self):

        self.real = talib.SMA(real=self.np_array, timeperiod=self.timeperiod)
        return self.real


class RSI(Indicator):

    def __init__(self, timeperiod=14, index=4, weight=False):
        super(RSI, self).__init__(index=index, weight=weight)
        self.timperiod = timeperiod
        self.real = []

    def get_RSI(self):

        self.real = talib.RSI(real=self.np_array, timeperiod=self.timperiod)
        return self.real


class EMA(Indicator):

    def __init__(self, time_period=12, index=4, weight=True):
        super(EMA, self).__init__(index=index, weight=weight)
        self.timeperiod = time_period
        self.real = []

    def get_EMA(self):

        self.real = talib.EMA(real=self.np_array, timeperiod=self.timeperiod)
        return self.real


class Momentum(Indicator):

    def __init__(self, time_period=2, index=4, weight=True):
        super(Momentum, self).__init__(index=index, weight=weight)
        self.timeperiod = time_period
        self.real = []

    def get_Momentum(self):

        self.real = talib.MOM(real=self.np_array, timeperiod=self.timeperiod)
        return self.real
