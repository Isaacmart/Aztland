import cbpro
import Data


key = Data.API_Public_Key
b64secret = Data.API_Secret_Key
passphrase = Data.Passphrase

trader_client = cbpro.AuthenticatedClient(key, b64secret, passphrase)

to_write = open("files/get_accounts.txt", "w")

data = trader_client.get_accounts()

for line in data:
    to_write.write(str(line) + "\n")