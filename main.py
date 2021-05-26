from get_currencies import trader_robot
import csv, json, pandas


data = trader_robot.get_products()

cvs_file = open('csv_files/get_products.csv', 'w')

new_writer = csv.writer(cvs_file, delimiter=',')

for value in data:
    value = pandas.read_json(value)
    value = pandas.to_csv
    print(value)
    #new_writer.writerow(value)
