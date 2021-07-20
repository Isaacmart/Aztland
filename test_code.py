from cbpro import AuthenticatedClient
from order import Order
from cbpro import PublicClient
from open_position import OpenPosition
from capital import Capital
from app_methods import *
from indicators import *
import Data

key = Data.API_Public_Key
b64secret = Data.API_Secret_Key
passphrase = Data.Passphrase

client = AuthenticatedClient(key, b64secret, passphrase)

pclient = PublicClient()

indicator = Indicator(client=pclient)
indicator.set_candles(product="MkR-USD", callback=get_time(27976), begin=get_time(0), granularity=300)
indicator.get_data_set()
indicator.reverse_data()
indicator.get_np_array()
macd_5m = MACD(client=pclient)
macd_5m.np_array = indicator.np_array
macd_5m.get_MACD()
volume_5m = VolSMA(client=pclient, timeperiod=20)
volume_5m.candles = indicator.candles
volume_5m.get_data_set()
volume_5m.reverse_data()
volume_5m.get_np_array()
volume_5m.get_volume()
print(volume_5m.get_volume())














