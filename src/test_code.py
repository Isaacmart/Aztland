from indicators import Indicator
from indicators import MACD
from indicators import BB
from indicators import RSI
from indicators import VolSMA
from indicators import EMA
from indicators import Momentum
from cbpro import AuthenticatedClient

data = open("../../data_5m/TRIBE-USD_5m.csv", "r")
for line in data:
    print(line)