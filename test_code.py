from indicators import *
from app_methods import *
from cbpro import PublicClient
from cbpro import AuthenticatedClient
import Data
from capital import Capital

key = Data.API_Public_Key
b64secret = Data.API_Secret_Key
passphrase = Data.Passphrase


client = AuthenticatedClient(key, b64secret, passphrase)
capital = Capital(client)
print(capital.set_capital())
