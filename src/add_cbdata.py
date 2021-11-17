import csv
import time
from numpy import random


granularity = 60

data = None
index = 0
last_line: str
last_date: float
try:
    data = open("../../data_1m/BT-USD_1m.csv", "r")
    reader = csv.reader(data)
    for line in reader:
        if index < 2:
            last_line = line
            index += 1
        else:
            break
    last_date = float(last_line[0])
    diff = time.time() - last_date
    req = diff / granularity
    max_req = req / 300
    print(last_date)
    print(diff)
    print(req)
    print(max_req)
except FileNotFoundError as fnfe:
    print("No such file")
