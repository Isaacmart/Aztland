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
        self.indicator_values = []
        self.np_array = numpy.ndarray([])
        self.name = name
        self.timeline = timeline
        self.lock = Lock()
        self.analyze = True

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
            self.candlesticks.pop(-1)
            return True
        except IndexError:
            return False

    #Adds a candlestick to the list
    def candle_prepend(self, candle):
        if self.candle_pop():
            self.candlesticks.insert(0, candle)

    #Makes a request to Coinbase for historical data
    def candle_start(self, callback=94, begin=0):

        if callback < 300:
            cb = get_time(callback * self.timeline)
            bn = get_time(begin)
            self.candlesticks = self.indicator.set_candles(self.name, cb, bn, self.timeline)
            if type(self.candlesticks) == list:
                l = len(self.candlesticks)
                if l < 94:
                    self.candle_start(callback=callback + (94-l))
                else:
                    return
            else:
                time.sleep(.50)
                self.candle_start(callback=callback)
                    
        else:
            self.analyze = False
            return

    #Takes a json object and returns timestamp, price, volume
    def candle_create(self, js_obj):
        timestamp = 0.0
        price = 0.0
        vol = 0.0

        if "time" in js_obj:
            a_str = js_obj["time"]
            n_str = a_str.replace("Z", "+00:00")
            timestamp = int(datetime.fromisoformat(n_str).timestamp())
        else:
            timestamp = time.time()

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

        # reference to latest candle in the list
        last_candle = list(self.candlesticks)[0]

        if timestamp >= (float(last_candle[0]) + self.timeline):
            #Creates new candle and populates it with data from the last trade
            #[time, low, high, open, close, volume]
            ts = timestamp - (timestamp % self.timeline)
            new_candle = [ts, price, price, price, price, vol]
            #Insert candle into candlesticks
            self.candle_prepend(new_candle)

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

    #Calculates the given indicator
    def calculate_indicator(self, indicator: Indicator):
        indicator.np_array = self.indicator.np_array
        indicator.set_indicator()
        values = indicator.get_index(-1)

        if type(values) is list:
            self.indicator_values.extend(values)

        else:
            self.indicator_values.append(values)

    def read_indicators(self):
        self.indicator.set_indicator()
        self.indicator_values = []

        for indicator in self.indicators:
            self.calculate_indicator(indicator)

        print(self.name, self.timeline, self.indicator_values)
