import csv
import pytz
from datetime import datetime
import time


def write_to_csv(a_string):
    to_write = open('webhook_log.csv', 'w')
    writer = csv.writer(to_write)
    writer.writerow(a_string)
    to_write.close()


def get_time(amount):
    tz = pytz.timezone('US/Eastern')
    _time = datetime.fromtimestamp(time.time() - amount, tz).isoformat()
    return _time
