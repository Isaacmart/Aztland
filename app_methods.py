import csv
import pytz
from datetime import datetime
import time


#multiple methods used throughout the program

#Receives a_string to write to csv file
def write_to_csv(a_string):
    to_write = open('webhook_log.csv', 'w')
    writer = csv.writer(to_write)
    writer.writerow(a_string)
    to_write.close()


#Amount equals seconds to go back to take time, returns
#actual time is zero
def get_time(amount):
    tz = pytz.timezone('US/Eastern')
    _time = datetime.fromtimestamp(time.time() - amount, tz).isoformat()
    return _time


#Gets a flask.request ticker key and returns a matching product in coinbase
def get_ticker_product(new_request):
    new_ticker = new_request['ticker']
    new_coin = new_ticker[0:-3]
    coin_currency = new_ticker[-3:]
    ticker_product = new_coin + "-" + coin_currency
    return ticker_product
