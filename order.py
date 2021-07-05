import Data
import time
from cbpro.authenticated_client import AuthenticatedClient

'''
key = Data.API_Public_Key
b64secret = Data.API_Secret_Key
passphrase = Data.Passphrase
'''

'''Collects the data from the order response
and packs it into a single data structure to
facilitate its use in other places'''


class Order:

    def __init__(self):
        self.id = None
        self.size = None
        self.product = None
        self.side = None
        self.funds = None
        self.done_at = None
        self.executed_value = None
        self.status = None





'''
Example of get_order() response:

{
    "id": "68e6a28f-ae28-4788-8d4f-5ab4e5e5ae08",
    "size": "1.00000000",
    "product_id": "BTC-USD",
    "side": "buy",
    "stp": "dc",
    "funds": "9.9750623400000000",
    "specified_funds": "10.0000000000000000",
    "type": "market",
    "post_only": false,
    "created_at": "2016-12-08T20:09:05.508883Z",
    "done_at": "2016-12-08T20:09:05.527Z",
    "done_reason": "filled",
    "fill_fees": "0.0249376391550000",
    "filled_size": "0.01291771",
    "executed_value": "9.9750556620000000",
    "status": "done",
    "settled": true
}
'''

