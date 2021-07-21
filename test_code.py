from dict import new_dict
from order import Order
from app_methods import *
import Data
from cbpro import AuthenticatedClient
import math

key = Data.API_Public_Key
b64secret = Data.API_Secret_Key
passphrase = Data.Passphrase

client = AuthenticatedClient(key, b64secret, passphrase)

new_order = Order(client)
new_order.new_id = "36dfc4e9-9826-45dd-bcb3-268cc67e0b79"
new_order.set_details()

size = get_size(new_order.get_key("product_id"), new_order.get_key('filled_size'))
print(size)
print(new_order.get_key("product_id"))
print(new_order.get_key('filled_size'))
print(round_down(float(new_order.get_key('filled_size')), 2))


