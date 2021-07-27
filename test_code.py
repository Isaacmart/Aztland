from dateutil import parser
from cbpro import AuthenticatedClient
import Data
from app_methods import *
import time
t = "1984-06-02T19:05:00.000Z"
new_id = "fb2c32da-3c0d-47aa-923a-7b04a757b1a6"

key = Data.API_Public_Key
b64secret = Data.API_Secret_Key
passphrase = Data.Passphrase


client = AuthenticatedClient(key, b64secret, passphrase)


new_trade = client.get_order(new_id)

unix_time = get_unix(new_trade['done_at'])


if time.time() > (get_unix(new_trade['done_at']) + 900):
    print(True)
else:
    print(unix_time + 900)
    print(time.time())