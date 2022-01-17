import csv

file_name = open("../../data_1m/AGLD-USD_1m.csv")
reader = csv.reader(file_name)


previous = 0

for line in reader:
    try :
        current = int(line[0])
        if current > previous:
            print(current)
        previous = current
    except ValueError as ve:
        continue