from indicators import Indicator
from indicators import MACD
from indicators import BB
from indicators import RSI
from indicators import VolSMA
from indicators import EMA
from indicators import Momentum
from cbpro import AuthenticatedClient
import Data

client = AuthenticatedClient(Data.API_Public_Key, Data.API_Secret_Key, Data.Passphrase)

try:
    data = client.get_account('42d739b5-f5cd-48c0-baf6-b905836a1ca4')
    print(data)
except Exception as e:
    print(e)