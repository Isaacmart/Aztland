from indicators import Indicator
from indicators import BB
from indicators import MACD
from indicators import RSI
from indicators import VolSMA
from cbpro import PublicClient
from util import get_time
import csv

rows = []

indicator = Indicator()
indicator.set_candles("ETH-USD", get_time(18000), get_time(0), 60)
indicator.set_indicator()
print(indicator.np_array)
np_array = indicator.np_array

bb2 = BB()
bb1 = BB(ndbevup=1, nbdevdn=1)
macd = MACD()
rsi = RSI()
smavol= VolSMA()
indics = [bb2, bb1, macd, rsi, smavol]

for indic in indics:
    indic.set_indicator(np_array)

for indic in indics:
    if type(indic.get_indicator()) == tuple:
        for line in indic.get_indicator():
            print(len(line))
    else:
        print(len(indic.get_indicator()))

l = len(indicator.candles)
print(l)
for i in range(l-1):
    new_row = []
    new_row.extend(indicator.candles[i])
    for indic in indics:
        values = indic.get_index(i)
        for key in values:
            new_row.append(values[key])
    rows.append(new_row)


header = ['time', 'low', 'high', 'open', 'close', 'volume']
for indic in indics:
    values = indic.get_index(-1)
    for key in values:
        header.append(key)
f = open("../../model_data_test/eth-usd.csv", "w")
writer = csv.writer(f)
writer.writerow(header)
for row in rows:
    writer.writerow(row)

f.close()