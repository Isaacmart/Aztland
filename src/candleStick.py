from datetime import datetime
from app_methods import get_time
from indicators import Indicator
from candleTest import CandleTest
from threading import Thread
from threading import Lock
from numpy import ndarray
import time
import numpy


#Represents a candlestick lists
class CandleStick(Indicator):

    #Creates candlesticks for the given name and timeline
    def __init__(self, name, timeline):
        super(CandleStick, self).__init__()
        self.analysis = CandleTest(name, timeline)
        self.name = name
        self.timeline = timeline
        self.analyze = True
        self.lock = Lock()

    #Returns the name of this candlesticks when referenced
    def __str__(self):
        return self.name

    #Checks whether there are candlesticks already in the list
    def candle_started(self):

        try:
            start = self.candles[0]
            if type(start) == list:
                return True

        except IndexError:
            return False

    #Updates the latest candlestick
    def candle_update(self, price, volume):

        # Updates low price if this price is lower
        if price < self.candles[-1][1]:
            self.candles[-1][1] = price

        # Updates the high price if this price is higher
        elif price > self.candles[-1][2]:
            self.candles[-1][2] = price

        # Updates the closing price to this price
        self.candles[-1][4] = price
        # Add this volume to the overall volume for the timeline
        self.candles[-1][5] = self.candles[1][5] + volume

    #Makes a request to Coinbase for historical data
    def candle_start(self, callback=94, begin=0):

        if callback <= 300:
            cb = get_time(callback * self.timeline)
            bn = get_time(begin)
            self.set_candles(self.name, cb, bn, self.timeline)

            if type(self.candles) == list:
                l = len(self.candles)

                if l < 94:
                    nc = callback * (1 + (100 - ((l * 100) / callback)))
                    self.candle_start(callback=int(nc))

                else:
                    return

            else:
                time.sleep(.10)
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
            timestamp = float(datetime.fromisoformat(n_str).timestamp())

        else:
            timestamp = time.time()

        if "price" in js_obj:
            price = float(js_obj["price"])

        if "size" in js_obj:
            vol = float(js_obj["size"])

        return timestamp, price, vol

    def reset_analyze(self):

        if not self.analyze:

            if len(self.candles) > 94:
                self.analyze = True

    #Takes a json object to modify the candlesticks
    def candle_input(self, js_obj):

        with self.lock:
            timestamp, price, vol = self.candle_create(js_obj)

            # Populates the candlestick list if is empty
            if not self.candle_started():
                self.candle_start()

            if timestamp >= (float(self.candles[-1][0]) + self.timeline):

                if self.analyze:
                    self.make_test()
                    print(self.analysis.values)

                # Creates new candle and populates it with data from the last trade
                # [time, low, high, open, close, volume]
                ts = timestamp - (timestamp % self.timeline)
                new_candle = [ts, price, price, price, price, vol]
                # Insert candle into candlesticks
                self.candle.append(new_candle)
                self.reset_analyze()

            else:
                # Updates last candle
                self.candle_update(price, vol)

    #Makes a new test for this candlestick
    def make_test(self):
        #Updates the np_array for this candlesticks
        self.set_indicator()
        #Records the time for when the test was made
        self.analysis.update_time(self.candles[-1][0])
        #Passes the np array to the indicators and makes math
        self.analysis.test(self.np_array)
