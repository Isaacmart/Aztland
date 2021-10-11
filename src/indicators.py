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
        Coinbase yields data in queue, that is latest last; however, to get accurate numbers,
        the data passed to the indicators must be latest data last

        :return: List with closing prices reversed
        """
        self.close_array.reverse()
        return self.close_array

    def get_dates(self):
        """
        Puts of the dates in a list an reverses it the same method. That is because when we
        testing strategies sometimes we wanna see when it happened and we this method we just have to
        reference the same index as the one in the closing prices list

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
        Ta-Lib takes data in a numpy array, this method coverts a regular list into a numpy array

        :return: Numpy array of closing prices
        """
        self.np_array = numpy.array(self.close_array)
        return self.np_array

    def crossover(self, x=[], y=[]):
        """
        Checks whether a value is crossing over another
        :param x: List that is crossing a value
        :param y: List that is being crossed

        :return:List of boolean values
        """
        cross_over = []
        i = 1
        while i < len(x):
            if (x[i] > y[i]) and (x[i - 1] < y[i - 1]):
                cross_over.insert(i, True)
            else:
                cross_over.insert(i, False)
        return cross_over

    def crossunder(self, x=[], y=[]):
        """
        Measures if a value is crossing another one under
        :param x: List crossing y
        :param y: List being crossed

        :return: List of boolean values
        """
        cross_under = []
        i = 1
        while 1 < len(x):
            if (x[i] < y[i]) and (x[i - 1] > y[i - 1]):
                cross_under.insert(i, True)
            else:
                cross_under.insert(i, False)
        return cross_under

    def set_indicator(self):
        pass

    def get_index(self, index):
        return self.close_array[index]


class MACD(Indicator):
    """
    Child class of Indicator that implements the Moving Average Convergence Divergence indicator

    MACD = fastperiod - slowperiod

    Histogram = Exponential moving average (12-period default)

    Histogram = MACD - Histogram
    """

    def __init__(self, fastperiod=12, slowperiod=26, signalperiod=9, index=4, weight=True):
        """
        Creates an instance variable of MACD class
        :param fastperiod: period of fast exponential moving average
        :param slowperiod: period of slow EMA
        :param signalperiod: period of exponential moving average used as trigger line
        :param index: index from where to get the data
        :param weight:
        """
        super(MACD, self).__init__(index=index, weight=weight)
        self.macd = []
        self.hist = []
        self.signal = []
        self.fast_period = fastperiod
        self.slow_period = slowperiod
        self.signal_period = signalperiod

    def set_indicator(self):
        self.macd, self.signal, self.hist = talib.MACD(real=self.np_array, fastperiod=self.fast_period, slowperiod=self.slow_period, signalperiod=self.signal_period)

    def get_indicator(self):
        return self.macd, self.signal, self.hist

    def get_index(self, index):
        real = [float(self.macd[index]), float(self.signal[index]), float(self.hist[index])]
        return real


class BB(Indicator):
    """
    Child class of Indicator that calculates Bollinger Bands from a list of values
    """

    def __init__(self, timeperiod=5, ndbevup=2, nbdevdn=2, matype=0, index=4, weight=False):
        """
        Creates an instance variable of class BB
        :param timeperiod: Time period of the Bollinger Bands
        :param ndbevup: Number of standard deviations for the upper band
        :param nbdevdn: Number of standard deviations for the lower band
        :param matype: Number of moving averages
        :param index: Index of Indicator.candles to get the data from
        :param weight: False if the indicator does not use Moving Averages
        """
        super(BB, self).__init__(index=index, weight=weight)
        self.upperband = []
        self.middleband = []
        self.lowerband = []
        self.timeperiod = timeperiod
        self.ndbevup = ndbevup
        self.nbdevdn = nbdevdn
        self.matye = matype

    def set_indicator(self):
        """
        Calculates the Bollinger Bands upper, middle, and lower bands
        :return:
        """
        self.upperband, self.middleband, self.lowerband = talib.BBANDS(real=self.np_array, timeperiod=self.timeperiod, nbdevup=self.ndbevup, nbdevdn=self.nbdevdn, matype=self.matye)

    def get_indicator(self):
        return self.upperband, self.middleband, self.lowerband

    def get_index(self, index):
        real = [float(self.upperband[index]), float(self.middleband[index]), float(self.lowerband[index])]
        return real


class VolSMA(Indicator):
    """
    Child class of Indicator that calculates volume's Simple Moving Average
    """

    def __init__(self, timeperiod=30, index=5, weight=False):
        """
        Creates an instance variable of class VolSMA
        :param timeperiod: The time period of the volume's SMa
        :param index: Index of Indicator.candles to get the data from
        :param weight: Defines if the indicator uses Exponential Moving Average
        """
        super(VolSMA, self).__init__(index=index, weight=weight)
        self.timeperiod = timeperiod
        self.real = []

    def set_indicator(self):
        """
        Calculates the moving average of the volume
        """
        self.real = talib.SMA(real=self.np_array, timeperiod=self.timeperiod)

    def get_indicator(self):
        return self.real

    def get_index(self, index):
        return float(self.real[index])


class RSI(Indicator):
    """
    Child class of Indicator used to calculate the Relative Strength index
    """

    def __init__(self, timeperiod=14, index=4, weight=False):
        """
        Creates an instance variable of class RSI
        :param timeperiod: Time period of the indicator
        :param index: Index of Indicator.candles to get the data from
        :param weight: False if the indicator does not use exponential moving averages
        """
        super(RSI, self).__init__(index=index, weight=weight)
        self.timperiod = timeperiod
        self.real = []

    def set_indicator(self):
        """
        Calculates the Relative Strength Index from the array passed
        """
        self.real = talib.RSI(real=self.np_array, timeperiod=self.timperiod)

    def get_indicator(self):
        return self.real

    def get_index(self, index):
        return float(self.real[index])


class EMA(Indicator):

    def __init__(self, time_period=12, index=4, weight=True):
        super(EMA, self).__init__(index=index, weight=weight)
        self.timeperiod = time_period
        self.real = []

    def set_indicator(self):
        self.real = talib.EMA(real=self.np_array, timeperiod=self.timeperiod)

    def get_indicator(self):
        return self.real

    def get_index(self, index):
        return float(self.real[index])


class Momentum(Indicator):

    def __init__(self, time_period=2, index=4, weight=True):
        super(Momentum, self).__init__(index=index, weight=weight)
        self.timeperiod = time_period
        self.real = []

    def set_indicator(self):
        self.real = talib.MOM(real=self.np_array, timeperiod=self.timeperiod)

    def get_indicator(self):
        return self.real

    def get_index(self, index):
        return float(self.real[index])
