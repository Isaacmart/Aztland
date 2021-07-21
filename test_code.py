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
new_order.new_id = "ecb6d574-5498-4c0d-a971-8d7dea00a412"
new_order.set_details()

size = get_size(new_order.get_key("product_id"), new_order.get_key('filled_size'))
print(size)
print(new_order.get_key("product_id"))
print(new_order.get_key('filled_size'))
print(round_down(float(new_order.get_key('filled_size')), 2))


