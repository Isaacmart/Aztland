import numpy
import talib
from cbpro import PublicClient
from threading import Lock
from collections import deque


class Indicator:
    """
    Base class for any indicator.\n
    Coinbase returns data in the following way:\n
    [1415398768, 0.32, 4.2, 0.35, 4.2, 12.3],\n
    Indicator work with close prices as default, therefore we append data from index 4.\n
    If the indicator is weighted, certain amount of elements back are needed,
    weight = True will get that many elements automatically
    """

    def __init__(self, index=4, weight=True, max_length=0):
        """
        Creates an instance of the Indicator class\n
        Args:
             index (int): type of price to work with, close price is default
             weight (bool): If
        """
        if max_length:
            self.candles = deque(maxlen=max_length)
            self.close_array = deque(maxlen=max_length)
            self.date_array = deque(maxlen=max_length)
        else:
            self.candles = deque()
            self.close_array = deque()
            self.date_array = deque()
        self.np_array = []
        self.index = index
        self.weight = weight

    def __str__(self):
        return "indicator"

    def set_candles(self, product, callback, begin, granularity):
        """
        Makes requests to the Coinbase API for Historic rates\n
        Args:
            product (str): A valid Coinbase product
            callback (int):  Number of seconds to go back from begin
            begin (int): Last second to get rates from
            granularity (int): Number of seconds
        """

        client = PublicClient(timeout=45)
        new_candles = client.get_product_historic_rates(product_id=product, start=callback, end=begin,
                                                        granularity=granularity)

        bound = len(new_candles)

        for i in range(bound):
            self.candles.appendleft(new_candles[i])

        return self.candles

    def set_dates(self):
        """
        Puts of the dates in a list an reverses it the same method. That is because when we
        testing strategies sometimes we wanna see when it happened and we this method we just have to
        reference the same index as the one in the closing prices list.\n
        :return: Reversed list of dates in Unix form
        """
        l = len(self.candles)
        for p in range(l):
            self.date_array.append(self.candles[p][0])
        return self.date_array

    def set_indicator(self, array=None):

        if array is None:
            for candle in self.candles:
                self.close_array.append(float(candle[self.index]))
            self.np_array = numpy.array(self.close_array)

        else:
            self.np_array = array

    def get_indicator(self):
        return self.np_array

    def get_index(self, index):
        return {"price": float(self.close_array[index])}

    def price(self):
        return self.close_array[-1]


class MACD(Indicator):
    """
    Child class of Indicator that implements the Moving Average Convergence Divergence indicator.\n
    MACD = fastperiod - slowperiod\n
    Histogram = Exponential moving average (12-period default)\n
    Histogram = MACD - Histogram\n
    """

    def __init__(self, fastperiod=12, slowperiod=26, signalperiod=9, index=4, weight=True):
        """
        Creates an instance variable of MACD class.\n
        Args:
            fastperiod: period of fast exponential moving average
            slowperiod: period of slow EMA
            signalperiod: period of exponential moving average used as trigger line
            index: index from where to get the data
            weight: whether the Indicator is weighted or not.
        """
        super(MACD, self).__init__(index=index, weight=weight)
        self.macd = []
        self.hist = []
        self.signal = []
        self.fast_period = fastperiod
        self.slow_period = slowperiod
        self.signal_period = signalperiod

    def __str__(self):
        return "MACD"

    def set_indicator(self, array=None):
        #super(MACD, self).set_indicator()
        if array is None:
            self.macd, self.signal, self.hist = talib.MACD(real=self.np_array, fastperiod=self.fast_period,
                                                           slowperiod=self.slow_period, signalperiod=self.signal_period)

        else:
            self.macd, self.signal, self.hist = talib.MACD(real=array, fastperiod=self.fast_period,
                                                           slowperiod=self.slow_period, signalperiod=self.signal_period)

    def get_indicator(self):
        return self.macd, self.signal, self.hist

    def get_index(self, index):
        return {
            "macd_macd": float(self.macd[index]),
            "macd_signal": float(self.signal[index]),
            "macd_hist": float(self.hist[index])
        }


class BB(Indicator):
    """
    Child class of Indicator that calculates Bollinger Bands from a list of values
    """

    def __init__(self, timeperiod=20, ndbevup=2, nbdevdn=2, matype=0, index=4, weight=False):
        """
        Creates an instance variable of class BB.\n
        Args:
            timeperiod: Time period of the Bollinger Bands
            ndbevup: Number of standard deviations for the upper band
            nbdevdn: Number of standard deviations for the lower band
            matype: Number of moving averages
            index: Index of Indicator.candles to get the data from
            weight: False if the indicator does not use Moving Averages
        """
        super(BB, self).__init__(index=index, weight=weight)
        self.upper = []
        self.middle = []
        self.lower = []
        self.bb_width = []
        self.sma_bbw = []
        self.pbb = []
        self.timeperiod = timeperiod
        self.ndbevup = ndbevup
        self.nbdevdn = nbdevdn
        self.matye = matype

    def __str__(self):
        return "BB"

    def set_indicator(self, array=None):
        """
        Calculates the Bollinger Bands upper, middle, and lower bands.\n
        :return:
        """
        #super(BB, self).set_indicator()
        if array is None:
            self.upper, self.middle, self.lower = talib.BBANDS(real=self.np_array, timeperiod=self.timeperiod,
                                                               nbdevup=self.ndbevup, nbdevdn=self.nbdevdn,
                                                               matype=self.matye)
            self.get_pBB(p_array=self.np_array)
        else:
            self.upper, self.middle, self.lower = talib.BBANDS(real=array, timeperiod=self.timeperiod,
                                                               nbdevup=self.ndbevup, nbdevdn=self.nbdevdn,
                                                               matype=self.matye)
            self.get_pBB(p_array=array)

        self.get_bbWidth()
        self.width_SMA()

    def get_indicator(self):
        return self.upper, self.middle, self.lower, self.pbb, self.bb_width, self.sma_bbw

    def get_index(self, index):
        return {
            f"bb{self.ndbevup}_upper": float(self.upper[index]),
            f"bb{self.ndbevup}_middle": float(self.middle[index]),
            f"bb{self.ndbevup}_lower": float(self.lower[index]),
            f"bb{self.ndbevup}_%bb": float(self.pbb[index]),
            f"bb{self.ndbevup}_width": float(self.bb_width[index]),
            f"bb{self.ndbevup}_sma(bbw)": float(self.sma_bbw[index])
        }

    def get_pBB(self, index=-1, p_array=None):
        for i in range(len(self.middle)):
            try:
                value = (p_array[i] - float(self.lower[i])) / (float(self.upper[i]) - float(self.lower[i]))
                self.pbb.append(value)
            except ValueError:
                self.pbb.append(0.0)
            except ZeroDivisionError:
                self.pbb.append(0.0)

    def get_bbWidth(self, index=-1):
        for i in range(len(self.middle)):
            try:
                value = (float(self.upper[i]) - float(self.lower[i])) / float(self.middle[i])
                self.bb_width.append(value)
            except ValueError:
                self.bb_width.append(0.0)
            except ZeroDivisionError:
                self.bb_width.append(0.0)

    def width_SMA(self):
        np_array = numpy.array(self.bb_width)
        self.sma_bbw = talib.SMA(real=np_array, timeperiod=self.timeperiod)


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

    def __str__(self):
        return "VolSMA"

    def set_indicator(self, array=None):
        """
        Calculates the moving average of the volume
        """
        #super()
        if array is None:
            self.real = talib.SMA(real=self.np_array, timeperiod=self.timeperiod)
        else:
            self.real = talib.SMA(real=array, timeperiod=self.timeperiod)

    def get_indicator(self):
        return self.real

    def get_index(self, index):
        return {"sma(vol)": float(self.real[index])}


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
        self.timeperiod = timeperiod
        self.real = []

    def __str__(self):
        return "RSI"

    def set_indicator(self, array=None):
        """
        Calculates the Relative Strength Index from the array passed
        """
        #super()
        if array is None:
            self.real = talib.RSI(real=self.np_array, timeperiod=self.timeperiod)
        else:
            self.real = talib.RSI(real=array, timeperiod=self.timeperiod)

    def get_indicator(self):
        return self.real

    def get_index(self, index):
        return {"rsi": float(self.real[index])}


class EMA(Indicator):

    def __init__(self, time_period=12, index=4, weight=True):
        super(EMA, self).__init__(index=index, weight=weight)
        self.timeperiod = time_period
        self.real = []

    def __str__(self):
        return "EMA"

    def set_indicator(self, array=None):
        #super()
        if array is None:
            self.real = talib.EMA(real=self.np_array, timeperiod=self.timeperiod)
        else:
            self.real = talib.EMA(real=array, timeperiod=self.timeperiod)

    def get_indicator(self):
        return self.real

    def get_index(self, index):
        return {"sma": float(self.real[index])}


class Momentum(Indicator):

    def __init__(self, time_period=2, index=4, weight=True):
        super(Momentum, self).__init__(index=index, weight=weight)
        self.timeperiod = time_period
        self.real = []

    def __str__(self):
        return "Momentum"

    def set_indicator(self, array=None):
        #super()
        if array is None:
            self.real = talib.MOM(real=self.np_array, timeperiod=self.timeperiod)
        else:
            self.real = talib.MOM(real=array, timeperiod=self.timeperiod)

    def get_indicator(self):
        return self.real

    def get_index(self, index):
        return {"momentum": float(self.real[index])}


class ROC(Indicator):

    def __init__(self, time_period=10, index=4, weight=False):
        super(ROC, self).__init__(index=index, weight=weight)
        self.time_period = time_period
        self.real = []

    def __str__(self):
        return "ROC"

    def set_indicator(self, array=None):
        #super()
        if array is None:
            self.real = talib.ROC(real=self.np_array, timeperiod=self.time_period)
        else:
            self.real = talib.ROC(real=array, timeperiod=self.time_period)

    def get_indicator(self):
        return self.real

    def get_index(self, index):
        return {"roc": float(self.real[index])}
