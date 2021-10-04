from indicators import Indicator
from indicators import MACD
from indicators import BB
from indicators import RSI
from indicators import VolSMA
from indicators import EMA
from indicators import Momentum
from cbpro import AuthenticatedClient
import csv

indicator = Indicator()
data=[]
file = open("../../data_5m/TRIBE-USD_5m.csv", newline='')
reader = csv.reader(file, delimiter=',')
for row in reader:
    try:
        candle = []
        for element in row:
            candle.append(float(element))
        data.append(candle)
    except ValueError as ve:
        print(ve)
        continue

indicator.candles = data[1:]
indicator.get_data_set()
indicator.reverse_data()
indicator.get_dates()
indicator.get_np_array()

macd_5m = MACD()
volume_5m = VolSMA(timeperiod=20)
bands_2dev = BB()
bands_1dev = BB(ndbevup=1, nbdevdn=1)
rsi_5m = RSI()
ema_12p = EMA()
momentum = Momentum()


indicatorList = [macd_5m, volume_5m, bands_2dev, bands_1dev, rsi_5m, ema_12p, momentum]
for a_indicator in indicatorList:
    a_indicator.candles = indicator.candles
    a_indicator.get_data_set()
    a_indicator.reverse_data()
    a_indicator.get_dates()
    a_indicator.get_np_array()
    a_indicator.set_indicator()
