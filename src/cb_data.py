from cbpro import PublicClient
from indicators import Indicator
from app_methods import get_time
from dict import new_dict
import csv
import time

#token = "ETH-USD"
times = [1, 5, 15, 60, 360, 1440]

for tim in times:

    for token in new_dict:

        file_name: str
        max_requests = 0
        if tim <= 60:
            max_requests = ((60/tim) * 17520)/300
            try:

            file_name = f"../../data_{str(tim)}m/{token}_{str(tim)}m.csv"
        else:
            max_requests = ((1440/tim) * 730)/300
            new_time = tim/60
            file_name = f"../../data_{str(new_time)}h/{token}_{str(new_time)}h.csv"

        indicator = Indicator()
        seconds = 300 * 60 * tim  # number of seconds in a request for 300 candles
        callback = seconds  # start requesting data from "seconds" seconds ago
        begin = 0  # stop requesting data at 0 seconds ago
        requests = 0  # number of request in the last second
        gra = tim * 60  # granularity in seconds
        print(token)

        data = []
        index = 0
        # Requests data from coinbase
        while index < int(max_requests):

            try:
                indicator.set_candles(product=token, callback=get_time(callback), begin=get_time(begin), granularity=gra)
                print(indicator.candles)
            except Exception as e:
                print("failed because of", e)
                pass
            print(index)
            requests = requests + 1

            if len(indicator.candles) > 0:
                for line in indicator.candles:
                    data.append(line)

            else:
                print(indicator.candles)
                break

            begin = callback
            callback = callback + seconds
            index += 1
            if requests == 9:
                time.sleep(1)
                requests = 0

        new_str = ["time", "low", "high", "open", "close", "volume"]
        awriter = open(file_name, "w")
        writer = csv.writer(awriter, delimiter=',', quotechar='"')
        writer.writerow(new_str)
        for line in data:
            writer.writerow(line)
        awriter.close()
