from indicators import *
from cbpro import PublicClient

client = PublicClient()
new_ticker = "ETH-USD"

indicator = Indicator(client=client)
indicator.set_candles(product=new_ticker, callback=get_time(83929), begin=get_time(0), granularity=900)

macd_15m = MACD(client=client)
volume_15m = VolSMA(client=client, timeperiod=20)
bands_2dev = BB(client=client)
bands_1dev = BB(client=client, ndbevup=1, nbdevdn=1)
rsi_15m = RSI(client=client)
ema_12p = EMA(client=client)

indicator.get_data_set()
indicator.reverse_data()
indicator.get_np_array()

macd_15m.np_array = indicator.np_array
macd_15m.get_MACD()

bands_2dev.np_array = indicator.np_array
bands_2dev.get_BB()

bands_1dev.np_array = indicator.np_array
bands_1dev.get_BB()

rsi_15m.np_array = indicator.np_array
rsi_15m.get_RSI()

ema_12p.np_array = indicator.np_array
ema_12p.get_EMA()

volume_15m.candles = indicator.candles
volume_15m.get_data_set()
volume_15m.reverse_data()
volume_15m.get_np_array()
volume_15m.get_volume()

lst = [10, 50, 75, 83, 98, 84, 32]

index = 0
iterator = -1
for line in reversed(indicator.data_array):
    index = index - 1
    iterator = iterator + 1
    if line < ema_12p.real[index]:
        print(indicator.candles[iterator])
    else:
        break

