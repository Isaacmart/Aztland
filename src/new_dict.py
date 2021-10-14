from cbpro import PublicClient

client = PublicClient()

writer = open("dict.py", "w")

data = client.get_products()

count = 0
writer.write("new_dict = {\n")

for line in data:
    if line['quote_currency'] == "USD":
        writer.write("    \"" + line['id'] + "\": \"" + str(len(line['base_increment']) - 2) + "\",\n")

writer.write("}")
