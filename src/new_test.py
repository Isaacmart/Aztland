from indicators import *
from datetime import datetime
import pytz
from app_methods import get_time

p_client = PublicClient()
indicator = Indicator()
indicator.initiate_client(p_client)

new_ticker = "AXS-USD"

_time = 1629145801

tz = pytz.timezone('US/Eastern')
finish = datetime.fromtimestamp(_time, tz).isoformat()
start = datetime.fromtimestamp(_time - 27976, tz).isoformat()

if True:
    try:
        indicator.set_candles(product=new_ticker, callback=start, begin=finish, granularity=300)
    except ValueError:
        print(new_ticker)
        print(indicator.candles)
        # wait to make another request
        pass


macd_5m = MACD()
volume_5m = VolSMA(timeperiod=20)
bands_2dev = BB()
bands_1dev = BB(ndbevup=1, nbdevdn=1)
rsi_5m = RSI()
ema_12p = EMA()
momentum = Momentum()


if len(indicator.candles) > 0:

    try:
        indicator.get_data_set()
        indicator.reverse_data()
        indicator.get_np_array()
    except Exception:
        print("indicators failed for: " + new_ticker)
        print(indicator.candles)

    try:
        macd_5m.np_array = indicator.np_array
        macd_5m.get_indicator()
    except Exception:
        print("macd failed for: " + new_ticker)
        print(indicator.candles)

    try:
        bands_2dev.np_array = indicator.np_array
        bands_2dev.get_indicator()
    except Exception:
        print("bands_2dev failed for: " + new_ticker)
        print(indicator.candles)

    try:
        bands_1dev.np_array = indicator.np_array
        bands_1dev.get_indicator()
    except Exception:
        print("bands_1dev failed for: " + new_ticker)
        print(indicator.candles)

    try:
        rsi_5m.np_array = indicator.np_array
        rsi_5m.get_indicator()
    except Exception:
        print("rsi failed for: " + new_ticker)
        print(indicator.candles)

    try:
        ema_12p.np_array = indicator.np_array
        ema_12p.get_indicator()
    except Exception:
        print("ema_12 failed for: " + new_ticker)
        print(indicator.candles)

    try:
        volume_5m.candles = indicator.candles
        volume_5m.get_data_set()
        volume_5m.reverse_data()
        volume_5m.get_np_array()
        volume_5m.get_indicator()
    except Exception:
        print("volume_ema failed for: " + new_ticker)
        print(indicator.candles)

    try:
        momentum.np_array = indicator.np_array
        momentum.get_indicator()

    except Exception as e:
        print("momentum failed for: ", new_ticker)
        print(e)

else:
    # try setting candles again
    pass


print(momentum.real)

