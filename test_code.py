from app_methods import get_time
from cbpro import PublicClient

client = PublicClient()

data = client.get_product_historic_rates(product_id="ETH-USD", start=get_time(27976), end=get_time(0), granularity=300)

index = 0
for line in data:
    index = index + 1

print(index)