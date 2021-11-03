from flask import Flask, request, abort, render_template, redirect, url_for
from open_position import OpenPosition
from order import Order
from capital import Capital
from cbpro import AuthenticatedClient
from cbpro import PublicClient
from indicators import Indicator
from indicators import MACD
from indicators import BB
from indicators import RSI
from indicators import VolSMA
from indicators import EMA
from indicators import Momentum
from app_methods import get_time
from app_methods import get_ticker
from app_methods import last_instance
from app_methods import get_size
from strategies import Strategy
import time
import Data
import csv

data = open("../../data_5m/AGLD-USD_5m.csv", "r")
new_reader = csv.reader(data)
candles = []
for line in new_reader:
    candles.append(line)

private_client = AuthenticatedClient(Data.API_Public_Key, Data.API_Secret_Key, Data.Passphrase)
new_order = Order(private_client)
indicator = Indicator()
macd_5m = MACD()
bands_1dev = BB(ndbevup=1, nbdevdn=1)
bands_2dev = BB()
volume_5m = VolSMA(timeperiod=20)
rsi_5m = RSI()
ema_12p = EMA()
momentum = Momentum()

indicator.candles = candles
indicator.get_data_set()
indicator.reverse_data()
indicator.get_dates()
indicator.get_np_array()

indicator_list = [macd_5m, volume_5m, bands_2dev, bands_1dev, rsi_5m, ema_12p, momentum]
for new_indicator in indicator_list:
    new_indicator.candles = candles
    new_indicator.get_data_set()
    new_indicator.reverse_data()
    new_indicator.get_dates()
    new_indicator.get_np_array()
    new_indicator.set_indicator()
    #print(new_indicator.get_index(-1))

# verifies that the data was extracted successfully
h = 0
y = -1
while h < 3:
    if indicator.date_array[h] == indicator.candles[y][0]:
        print(indicator.date_array[h].__class__)
        print(indicator.candles[y][0].__class__)
    else:
        raise ValueError("dates do not match")

    h = h + 1
    y = y - 1


l = 0
q = -1
while l < len(indicator.candles):
    if str(indicator.close_array[l]) == indicator.candles[q][4]:
        pass
    else:
        print(indicator.close_array[l])
        print(indicator.candles[q][4])
        print(l)
        print(q)
        raise ValueError("close prices do not match")
    l = l + 1
    q = q - 1
