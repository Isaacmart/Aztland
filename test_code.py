from cbpro import AuthenticatedClient
from capital import Capital

key = Data.API_Public_Key
b64secret = Data.API_Secret_Key
passphrase = Data.Passphrase

client = AuthenticatedClient(key, b64secret, passphrase)

funds = Capital(client)
funds.set_capital()
print(funds.get_capital())














