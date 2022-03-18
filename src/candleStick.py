from datetime import datetime
from app_methods import get_time
from indicators import Indicator
from indicators import MACD
from indicators import BB
from indicators import RSI
from indicators import EMA
from indicators import VolSMA
from threading import Thread
from threading import Lock
from numpy import ndarray
import time
import numpy


#Represents a candlestick lists
class CandleStick:

    def __init__(self, name, timeline):
        self.candlesticks = []
        self.indicator = Indicator()
        self.indicators = [MACD(), RSI(), BB(), BB(ndbevup=1, nbdevdn=1)]
        self.np_array = numpy.ndarray([])
        self.name = name
        self.timeline = timeline
        self.lock = Lock()

    def __str__(self):
        return self.name

    #Checks whether there are candlesticks already in the list
    def candle_started(self):
        try:
            start = self.candlesticks[0]
            return True
        except IndexError:
            return False

    #Deletes the oldest candlestick from the list
    def candle_pop(self):
        try:
            self.candlesticks.pop(0)
        except IndexError:
            return False

    #Adds a candlestick to the list
    def candle_append(self, candle):
        self.candle_pop()
        self.candlesticks.append(candle)

    #Replace a candlestick from the list
    def candle_replace(self, candle):
        try:
            self.candlesticks.pop(-1)
            self.candlesticks.append(candle)
        except IndexError:
            self.candlesticks.append(candle)

    #Makes a request to Coinbase for historical data
    def candle_start(self, callback=0, begin=0):
        cb = ""
        bn = ""
        if callback > 0:
            cb = callback
        else:
            cb = get_time(94 * self.timeline)

        if begin > 0:
            bn = begin
        else:
            bn = get_time(0)

        self.candlesticks = self.indicator.set_candles(self.name, cb, bn, self.timeline)
        self.indicator.set_indicator()

    #Takes a json object and returns timestamp, price, volume
    def candle_create(self, js_obj):
        timestamp = time.time()
        price = 0.0
        vol = 0.0
        if "time" in js_obj:
            a_str = js_obj["time"]
            n_str = a_str.replace("Z", "+00:00")
            timestamp = int(datetime.fromisoformat(n_str).timestamp())
        if "price" in js_obj:
            price = float(js_obj["price"])
        if "size" in js_obj:
            vol = float(js_obj["size"])

        return timestamp, price, vol

    #Takes a json object to modify the candlesticks
    def candle_input(self, js_obj):
        timestamp, price, vol = self.candle_create(js_obj)

        #Populates the candlestick list if is empty
        if not self.candle_started():
            self.candle_start()

        # reference to the last candle in the list
        last_candle = self.candlesticks[0]

        if timestamp >= (last_candle[0] + self.timeline):
            #Creates new candle and populates it with data from the last trade
            #[time, low, high, open, close, volume]
            ts = timestamp - (timestamp % self.timeline)
            new_candle = [ts, price, price, price, price, vol]
            self.candlesticks.insert(0, new_candle)
            self.candlesticks.pop(-1)
            self.indicator.set_indicator()
            print("new candle", time.time())

        else:
            #Updates last candle
            self.candle_update(price, vol, last_candle)

    def candle_update(self, price, volume, last_candle: list):
        # Updates low price if this price is lower
        if price < last_candle[1]:
            last_candle[1] = price

        # Updates the high price if this price is higher
        elif price > last_candle[2]:
            last_candle[2] = price

        # Updates the closing price to this price
        last_candle[4] = price
        # Add this volume to the overall volume for the timeline
        last_candle[5] = last_candle[5] + volume
        self.indicator.set_indicator()

    #Replaces a value in the ndarray used to calculate indicators
    def ndarray_replace(self, value, index=-1):
        self.np_array[index] = value

    #Eliminates and adds a value at the specified index
    def ndarray_add(self, value, index=-1):
        self.np_array.take(0)
        self.np_array.put(index, value)

    #Calculates the given indicator
    def calculate_indicator(self, indicator: Indicator):
        indicator.lock.acquire()
        indicator.np_array = self.indicator.np_array
        indicator.set_indicator()
        print(self.name, self.timeline, indicator.get_index(-1))
        indicator.lock.release()

    def read_indicators(self):
        for indicator in self.indicators:
            thread = Thread(target=self.calculate_indicator, args=[indicator])
            thread.start()
