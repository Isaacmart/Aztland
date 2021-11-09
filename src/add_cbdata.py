import csv
import time
from numpy import random

data = open("../../data_1m/BTC-USD_1m.csv", "r")
last_line: str
reader = csv.reader(data)

index = 0
total_amount = 0
for line in reader:
    try:
        total_amount += float(line[4])
    except ValueError as ve:
        continue
    index += 1

random.normal()

print(total_amount/index)
