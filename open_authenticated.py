import Data
import time
from cbpro.authenticated_client import AuthenticatedClient

'''
key = Data.API_Public_Key
b64secret = Data.API_Secret_Key
passphrase = Data.Passphrase
'''

#Collects the data from the order response
#and packs it into a single data structure to
#facilitate its use in other places


class Order:

    def __init__(self):
        self.id = None
        self.funds = None
        self.product = None
        self.status = None
        self.size = None
        self.fill_time = None
        self.executed_value = None
        self.side = None



'''
client = AuthenticatedClient(key, b64secret, passphrase)

new_order = Order()

track_trade = client.place_market_order(product_id="ETH-USD", side="buy", funds="5.00")
new_order.id = track_trade.get("id")

track_order = client.get_order(str(new_order.id))

new_order.status = track_order.get("done_reason")

if new_order.status is not None:

    new_order.side = track_order.get("side")
    new_order.product = track_order.get("product_id")
    new_order.fill_time = track_order.get("done_at")
    new_order.executed_value = track_order.get("executed_value")
    new_order.size = order_size = track_order.get("filled_size")
    new_order.print_values()

else:
    print("waiting")
'''

'''
track_trade = client.place_market_order(product_id="ETH-USD", side="buy", funds="5.00")
trade_id = track_trade.get("id")


track_order = client.get_order(str(trade_id))
order_funds = track_order.get("funds")
order_product = track_order.get("product_id")
order_status = track_order.get("done_reason")
order_size = track_order.get("filled_size")
order_fill_time = track_order.get("done_at")

print(order_funds)
print(order_product)
print(order_status)
print(order_size)
print(order_fill_time)
'''

