import cbpro

trader_robot = cbpro.PublicClient()

to_write = open("../txt_files/get_currencies.txt", "w")

data = trader_robot.get_currencies()

for line in data:
    to_write.write(str(line) + "\n")
