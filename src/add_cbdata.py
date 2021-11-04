import os
import csv

data = open("../../data_15m/AGLD-USD_15m.csv", "r")
last_line: str
reader = csv.reader(data)
for line in reader:
    last_line = line

print(last_line)