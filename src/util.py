import csv
import flask
import pytz
from datetime import datetime
import time
import math
import os
from dict import new_dict
from Data import Time

#multiple methods used throughout the program


#Receives a_string to write to csv file
def write_to_csv(path: str, a_string: str):
    to_write = open(path, 'a')
    writer = csv.writer(to_write)
    writer.writerow(a_string)
    to_write.close()


#Converts a number into ISO 8601 from amount of seconds ago
#Amount equals seconds to go back to take time, returns
#actual time is zero
def get_time(amount):
    tz = pytz.timezone('US/Eastern')
    _time = datetime.fromtimestamp(time.time() - amount, tz).isoformat()

    return _time


#Gets a flask.request ticker key and returns a matching product in coinbase'''
def get_ticker(new_request: dict):
    ticker_product: str
    if "ticker" in new_request:
        new_ticker = new_request["ticker"]
        # limit is equal to -3 products quoted in USD
        new_coin = new_ticker[0:-3]
        coin_currency = new_ticker[-3:]
        ticker_product = new_coin + "-" + coin_currency

        return ticker_product


#Gets the number of seconds to go back based on a given period
def get_callback(weight=True, period=0, granularity=0):
    if weight:
        callback = (3.453877639 * (period + 1)) * granularity
    else:
        callback = period + 1

    return callback


#Rounds down a float number to a 'decimals' number of decimals
def round_down(n, decimals=0):
    if decimals >= 0:
        multiplier = 10 ** decimals
        round_n = math.floor(n * multiplier) / multiplier
    else:
        round_n = int(n)

    return round_n


#gets the size of a sell order
def get_size(ticker, size):
    if ticker in new_dict:
        new_size = round_down(float(size), int(new_dict[ticker]))
    else:
        new_size = size

    return new_size


#get unix time from ISO 8601
def get_unix(a_date):
    parsed_t = parser.parse(a_date)
    return parsed_t.timestamp()


#makes sure that there are no two consecutive requests made to coinbase
def last_instance():
    file_size = os.path.getsize(Time)
    reader = open(Time, "r")
    greater: bool
    if file_size > 0:
        if time.time() > (float(reader.read()) + 5):
            greater = True
        else:
            greater = False
    else:
        greater = False
    reader.close()

    return greater
