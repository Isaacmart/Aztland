from cbpro import AuthenticatedClient
import Data

private_client = AuthenticatedClient(Data.API_Public_Key, Data.API_Secret_Key, Data.Passphrase)
print(private_client.get_accounts())