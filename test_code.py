from indicators import *
from app_methods import *
from cbpro import PublicClient
from cbpro import AuthenticatedClient
import Data
from capital import Capital

new_request = {'exchange': 'COINBASE', 'ticker': "ETHUSD", 'price': '2091.5', 'volume': '40.0421003', 'hist': '0.0004361752785138', 'macd': '-0.7505213797057877', 'signal': '-0.7509575549843015', 'volumema': '4.8900000000067'}
client = PublicClient()

indicator = Indicator(client)
indicator.set_candles(product=get_key('ticker', new_request), callback=get_time(27976), begin=get_time(0),
                                  granularity=300)
indicator.get_data_set()
indicator.reverse_data()
indicator.get_np_array()
macd_5m = MACD(client=client)
macd_5m.np_array = indicator.np_array
macd_5m.get_MACD()
volume_5m = VolSMA(client=client, timeperiod=20)
volume_5m.candles = indicator.candles
volume_5m.get_data_set()
volume_5m.reverse_data()
volume_5m.get_np_array()
volume_5m.get_volume()

print(indicator.candles)
print(macd_5m.hist)
print(volume_5m.real)
