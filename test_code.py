from cbpro import AuthenticatedClient
from order import Order
from open_position import OpenPosition
import Data

key = Data.API_Public_Key
b64secret = Data.API_Secret_Key
passphrase = Data.Passphrase

client = AuthenticatedClient(key, b64secret, passphrase)

new_order = Order(client)
new_order.get_id()
new_order.set_details()
position = OpenPosition(new_order)
position.set_position()
print(position.get_position())












