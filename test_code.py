from indicators import *
from app_methods import *
from cbpro import PublicClient
from cbpro import AuthenticatedClient
import Data

key = Data.API_Public_Key
b64secret = Data.API_Secret_Key
passphrase = Data.Passphrase


client = AuthenticatedClient(key, b64secret, passphrase)
print(float(get_capital('42d739b5-f5cd-48c0-baf6-b905836a1ca4', client)) - .50)
