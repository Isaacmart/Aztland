from indicators import Indicator
from app_methods import get_time
from dict import new_dict
import csv
import time

#token = "UMA-USD"
product_data = []
for token in new_dict:
    seconds = 86400 * 300
    callback = seconds
    begin = 0
    gra = 86400

    indicator = Indicator()

    requests = 0
    data = []

    while True:
        try:
            indicator.set_candles(product=token, callback=get_time(callback), begin=get_time(begin), granularity=gra)
            requests = requests + 1
        except Exception as e:
            print("failed because of", e)

        if len(indicator.candles) > 1:
            for line in indicator.candles:
                data.append(line)
            #print(indicator.candles)
        else:
            #print(indicator.candles)
            break

        begin = callback
        callback = callback + seconds
        if requests == 9:
            time.sleep(1)
            requests = 0

    candle_number = 0
    for candle in data:
        candle_number += 1

    product_data.append([token, candle_number])

product_data.sort(key=lambda x:x[1], reverse=True)
writer = open("../txt_files/latest_products.txt", "w")
for line in product_data:
    writer.write(str(line) + "\n")

writer.close()


