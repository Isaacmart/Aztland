import cbpro
import time
import pytz
from datetime import datetime
import talib
import numpy


def get_time(amount):
    tz = pytz.timezone('US/Eastern')
    _time = datetime.fromtimestamp(time.time() - amount, tz).isoformat()
    return _time


def get_any_MACD(product, period, callback, a_granularity):
    data_array = []
    new_client = cbpro.PublicClient()
    candle = new_client.get_product_historic_rates(product_id=product, start=callback, end=get_time(), granularity=a_granularity)
    for line in candle:
        data_array.append(line[4])
    data_array.reverse()
    npy_array = numpy.array(data_array)
    macd, macdsignal, macdhist = talib.MACD(real=npy_array, fastperiod=12, slowperiod=26, signalperiod=9)
    new_dict =
    return new_dict




new_socket = cbpro.PublicClient()
to_write = open("files/get_product_historic_rates.txt", "w")
data =  new_socket.get_product_historic_rates(product_id="ETH-USD", start=get_time(5580), end=get_time(0), granularity=60)
to_write.write("[ time, low, high, open, close, volume ], \n")
new_array = []
for line in data:
    to_write.write(str(line) + ",\n")
    new_array.append((line[4]))
new_array.reverse()
np_array = numpy.array(new_array)
macd, macdsignal, macdhist = talib.MACD(real=np_array, fastperiod=12, slowperiod=26, signalperiod=9)
print(new_array[-1])
print(macd[-1])
print(macdsignal[-1])
print(macdhist[-1])

