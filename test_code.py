from cbpro import PublicClient
from indicators import *

client = PublicClient()

indicator = MACD(client)

indicator.set_candles(product="ETH-USD", callback=get_time(83929), begin=get_time(0), granularity=900)

for candle in indicator.candles:

    if candle[4] < candle[3]:
        print(candle)


