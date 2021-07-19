from cbpro import AuthenticatedClient
from order import Order
from open_position import OpenPosition
import Data

key = Data.API_Public_Key
b64secret = Data.API_Secret_Key
passphrase = Data.Passphrase

client = AuthenticatedClient(key, b64secret, passphrase)

new_trade = client.place_market_order(product_id="ETH-USD", side="buy", funds=5.0)
writer = open("data.txt", "w")
writer.write(new_trade['id'])












