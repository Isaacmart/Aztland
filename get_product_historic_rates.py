import cbpro
import talib
import numpy
from webhookListener import get_time


class GetAnyMACD:

    #initiate variables
    def __init__(self):
        self.macd = 0.0
        self.hist = 0.0
        self.signal = 0.0
        self.candle = []
        self.new_client = cbpro.PublicClient()
        self.data_array = []

    #request candlesticks from coinbase
    #callback = get_time(amount) where amount is weights  * 3.45 * 60
    #new_gra is the granularity of the weigths in seconds, for example,
    #to get the macd for each minute the granularity will
    #be 60
    def set_candles(self, product, callback, new_gra):
        self.candle = self.new_client.get_product_historic_rates(product_id=product, start=callback, end=get_time(0), granularity=new_gra)

    #returns a list with the actual candlesticks
    def get_candles(self):
        return self.candle

    #Returns the macd from the list of candlesticks
    def set_any_MACD(self):

        for minute_candle in self.candle:
            self.data_array.append(minute_candle[4])

        #Obtain the most recent measure at the end
        self.data_array.reverse()

        #Convert to a type of array that can be processed by ta-lib
        npy_array = numpy.array(self.data_array)
        macd, macdsignal, macdhist = talib.MACD(real=npy_array, fastperiod=12, slowperiod=26, signalperiod=9)

        #Only get the most recent measures
        self.macd = macd[-1]
        self.signal = macdsignal[-1]
        self.hist = macdhist[-1]

    def get_macd(self):
        return self.macd

    def get_signal(self):
        return self.signal

    def get_hist(self):
        return self.hist


test5 = GetAnyMACD()
test5.set_candles(product="ETH-USD", callback=get_time(27945), new_gra=300)
test5.set_any_MACD()

test15 = GetAnyMACD()
test15.set_candles(product="ETH-USD", callback=get_time(83835), new_gra=900)
test15.set_any_MACD()


print(test5.get_hist())
print(test5.get_macd())
print(test5.get_signal())

print(test15.get_hist())
print(test15.get_macd())
print(test15.get_signal())

