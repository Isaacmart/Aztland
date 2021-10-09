from cbpro import AuthenticatedClient
import Data
from order import Order


private_client = AuthenticatedClient(Data.API_Public_Key, Data.API_Secret_Key, Data.Passphrase)
order_id = "84923794-d2d4-48d0-990f-4ea372a7b871"
data = private_client.get_order(order_id)
print(data)