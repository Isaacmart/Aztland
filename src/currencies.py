from cbpro import PublicClient


client = PublicClient()

currencies = client.get_currencies()

writer = open("../txt_files/get_currencies.txt", "w")

for line in currencies:
    writer.write(line)

writer.close()