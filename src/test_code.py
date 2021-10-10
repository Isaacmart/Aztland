from cbpro import AuthenticatedClient
import Data
from order import Order


private_client = AuthenticatedClient(Data.API_Public_Key, Data.API_Secret_Key, Data.Passphrase)
order_id = "d36c5c40-e8ea-4656-bb75-be0e02a22371"
data = private_client.get_order(order_id)
print(data)