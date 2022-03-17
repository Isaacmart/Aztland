import json
from dict import new_dict
from indicator import Indicator
from indicator import MACD
from indicator import BB
from indicator import RSI
from indicator import EMA
from indicator import VolSMA

from websocket import create_connection, WebSocketConnectionClosedException


#Represents a candlestick lists
class CandleStick:

    def __init__(self, name):
        self.candlesticks = []
        self.indicators = []
        self.name = name

    def __str__(self):
        return self.name

    #Checks whether there are candlesticks already in the list
    def candle_started(self):
        if self.candlesticks[0] > 0:
            return True
        else:
            return False

    #Deletes the oldest candlestick from the list
    def candle_pop(self):
        self.candlesticks.pop(0)

    #Adds a candlestick to the list
    def candle_append(self, candle):
        self.candle_pop()
        self.candlesticks.append(candle)

    #Replace a candlestick from the list
    def candle_replace(self, candle):
        self.candlesticks.pop(-1)
        self.candlesticks.append(candle)


#Populates a dict with classes using the keys from the products dict
def populate_dict(a_dict):
    cl_dict = {}
    for key in a_dict:
        cl_dict[key] = []
        cl_dict[key].append(CandleStick(key))
    return cl_dict


#access a candlesticks dict and gets the list representing the candlesticks for the product
def get_candlesticks(a_dict, product):
    try:
        a_candle = a_dict[product][0]
        return a_candle
    except ValueError as ve:
        return f"Tried to get candlesticks for {product}."


a_dict = {
    "ETH-USD": 1
}

n_dict = populate_dict(a_dict)
a_candle = get_candlesticks(n_dict, "ETH-USD")
print(a_candle)

