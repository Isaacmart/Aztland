from cbpro.public_client import PublicClient
from indicators import *

p_client = PublicClient()
indicator = Indicator()
indicator.initiate_client(p_client)


indicator.set_candles(product="XLM-USD", callback=get_time(27976), begin=get_time(0), granularity=300)

indicator.get_data_set()
indicator.reverse_data()
indicator.get_np_array()

macd_5m = MACD()
volume_15m = VolSMA(timeperiod=20)
bands_2dev = BB()
bands_1dev = BB(ndbevup=1, nbdevdn=1)
rsi_5m = RSI()
ema_12p = EMA()

macd_5m.np_array = indicator.np_array
macd_5m.get_MACD()

bands_2dev.np_array = indicator.np_array
bands_2dev.get_BB()

bands_1dev.np_array = indicator.np_array
bands_1dev.get_BB()
rsi_5m.np_array = indicator.np_array
rsi_5m.get_RSI()

ema_12p.np_array = indicator.np_array
ema_12p.get_EMA()

volume_15m.candles = indicator.candles
volume_15m.get_data_set()
volume_15m.reverse_data()
volume_15m.get_np_array()
volume_15m.get_volume()

print(volume_15m.real)