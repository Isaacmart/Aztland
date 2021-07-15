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
funds = Capital(client)
funds.set_capital()
new_order = Order(client=client)

#new_trade = client.place_market_order(product_id="ETH-USD", side="buy", funds=funds.get_capital())
new_order.set_details(new_id="8fe53ce3-0fdc-4b94-8906-16c075697d5")
print(funds.get_capital())
#print(new_trade)
print(new_order.set_details(new_id="8fe53ce3-0fdc-4b94-8906-16c075697d5"))
print(new_order.details)
