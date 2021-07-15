from indicators import *
from app_methods import *
from cbpro import PublicClient
from cbpro import AuthenticatedClient
import Data
from order import Order
from capital import Capital

key = Data.API_Public_Key
b64secret = Data.API_Secret_Key
passphrase = Data.Passphrase


client = AuthenticatedClient(key, b64secret, passphrase)

new_order = Order(client=client)
new_order.set_details(new_id="68e6a28f-ae28-4788-8d4f-5ab4e5e5ae08")
print(new_order.details)