from cbpro import PublicClient
from indicators import *
from app_methods import *

client = PublicClient()

indicator = Indicator()
indicator.initiate_client(client)
data = indicator.set_candles(product='ETH-USD', callback=get_time(27976), begin=get_time(0), granularity=300)
print(data)
