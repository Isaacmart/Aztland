from cbpro import AuthenticatedClient
import Data

private_client = AuthenticatedClient(Data.API_Public_Key, Data.API_Secret_Key, Data.Passphrase)
for line in private_client.get_accounts():
    if 'currency' in line:
        if line['currency'] == "USD":
            print(line["balance"]