from cbpro import PublicClient
from Data import *

client = PublicClient()

writer = open("products.py", "w")

data = client.get_products()

writer.write("links = {\n")

for line in data:
    if line['quote_currency'] == "USD":
        writer.write("    \"" + str(line['base_currency']) + str(line['quote_currency']) + "\": \"" + str(line["id"]) + ".csv\",\n")

writer.write("}")