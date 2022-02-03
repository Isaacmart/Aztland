from indicators import Indicator
from indicators import MACD
from app_methods import get_time
from dict import new_dict
import csv
import time

# token = "UMA-USD"
product_data = []
for token in new_dict:
    seconds = 86400 * 94
    callback = seconds
    begin = 0
    gra = 86400

    indicator = Indicator()

    requests = 0
    data = []

    try:
        indicator.set_candles(product=token, callback=get_time(callback), begin=get_time(begin), granularity=gra)
        print(indicator.candles[-1])
    except Exception as e:
        print(f"{token} failed because of ", e)

    macd = MACD()
    macd.candles = indicator.candles
    percentage: float
    try:
        macd.set_indicator()
        percentage = (macd.signal[-1] * 100) / macd.macd[-1]
        product_data.append([token, percentage, macd.signal[-1], macd.macd[-1]])
    except Exception as e:
        print(f"{token} failed because of ", e)
        percentage = 0


product_data.sort(key=lambda x:x[1], reverse=True)
writer = open("../txt_files/product_percentage", "w")
for line in product_data:
    writer.write(str(line) + "\n")

writer.close()


new_list = []
new_list.f
