from open_position import OpenPosition
from order import Order
from capital import Capital
from cbpro.authenticated_client import AuthenticatedClient
import Data

key = Data.API_Public_Key
b64secret = Data.API_Secret_Key
passphrase = Data.Passphrase


client = AuthenticatedClient(key, b64secret, passphrase)
new_order = Order.instance(client)
position = OpenPosition(new_order)
funds = Capital(client)
funds.set_capital()
