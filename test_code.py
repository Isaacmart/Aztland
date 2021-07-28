from cbpro import PublicClient
from app_methods import *

client = PublicClient()

data = client.get_product_historic_rates(product_id="ETH-USD", start=get_time(83929), end=get_time(0), granularity=900)

print(data)