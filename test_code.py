from cbpro import AuthenticatedClient
from order import Order
import Data

key = Data.API_Public_Key
b64secret = Data.API_Secret_Key
passphrase = Data.Passphrase

client = AuthenticatedClient(key, b64secret, passphrase)
new_order = Order(client)

writer = open("data.txt", 'r')

new_id = writer.read()

new_order.set_details(new_id)

print(new_order.details["id"])









