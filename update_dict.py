from dict import new_dict
from cbpro import PublicClient

client = PublicClient()

data = client.get_products()


for line in data:
    if line['quote_currency'] == "USD":
        if line['id'] in new_dict:
            pass
        else:
            print(line['id'])
