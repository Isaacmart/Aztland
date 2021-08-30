from strategies import Strategy
from cbpro import PublicClient
from cbpro import AuthenticatedClient
from order import Order
from open_position import OpenPosition
from dict import new_dict
from indicators import Indicator
from indicators import MACD
from indicators import VolSMA
from indicators import BB
from indicators import RSI
from indicators import EMA
from app_methods import get_time
from trade import Trade
import time
import Data

#token = "SOL-USD"

for token in new_dict:

    capital = 100
    client = PublicClient()
    a_client = AuthenticatedClient(Data.API_Public_Key, Data.API_Secret_Key, Data.Passphrase)
    indicator = Indicator()
    new_order = Order(a_client)
    new_order.get_id()
    new_order.set_details()
    position = OpenPosition(new_order)
    position.set_position()
    indicator.initiate_client(client)
    macd_5m = MACD()
    volume_5m = VolSMA(timeperiod=20)
    bands_2dev = BB()
    bands_1dev = BB(ndbevup=1, nbdevdn=1)
    rsi_5m = RSI()
    ema_12p = EMA()

    index = 0
    callback = 90000
    begin = 0

    data = []

    requests = 0
    print(token)

#Requests data from coinbase
    while index < 961:

        indicator.set_candles(product=token, callback=get_time(callback), begin=get_time(begin), granularity=300)
        requests = requests + 1

        if len(indicator.candles) > 0:
            for line in indicator.candles:
                data.append(line)

        else:
            break

        begin = callback
        callback = callback + 90000

        index = index + 1

        if requests == 9:
            time.sleep(1)
            requests = 0

    indicator.candles = data

    successful_exec = False

    try:
        indicator.get_data_set()
        indicator.reverse_data()
        indicator.get_dates()
        indicator.get_np_array()
        successful_exec = True
    except Exception:
        successful_exec = False
        print("indicators failed for: ", token)
        print(indicator.candles)

    try:
        macd_5m.np_array = indicator.np_array
        macd_5m.get_MACD()
        successful_exec = True
    except Exception:
        successful_exec = False
        print("macd failed for: " + token)
        print(indicator.candles)

    try:
        bands_2dev.np_array = indicator.np_array
        bands_2dev.get_BB()
        successful_exec = True
    except Exception:
        successful_exec = False
        print("bands_2dev failed for: " + token)
        print(indicator.candles)

    try:
        bands_1dev.np_array = indicator.np_array
        bands_1dev.get_BB()
        successful_exec = True
    except Exception:
        successful_exec = False
        print("bands_1dev failed for: " + token)
        print(indicator.candles)

    try:
        rsi_5m.np_array = indicator.np_array
        rsi_5m.get_RSI()
        successful_exec = True
    except Exception:
        successful_exec = False
        print("rsi failed for: " + token)
        print(indicator.candles)

    try:
        ema_12p.np_array = indicator.np_array
        ema_12p.get_EMA()
        successful_exec = True
    except Exception:
        successful_exec = False
        print("ema_12 failed for: " + token)
        print(indicator.candles)

    try:
        volume_5m.candles = indicator.candles
        volume_5m.get_data_set()
        volume_5m.reverse_data()
        volume_5m.get_np_array()
        volume_5m.get_volume()
        successful_exec = True
    except Exception:
        successful_exec = False
        print("volume_ema failed for: " + token)
        print(indicator.candles)

    # verifies that the data was extracted successfully
    h = 0
    y = -1

    while h < len(indicator.candles):
        if indicator.date_array[h] == indicator.candles[y][0]:
            pass
        else:
            print("error, dates do not match")

        h = h + 1
        y = y - 1

    l = 0
    q = -1

    while l < len(indicator.candles):

        if indicator.close_array[l] == indicator.candles[q][4]:
            pass
        else:
            print("error, close prices do not match")

        l = l + 1
        q = q - 1

    if successful_exec is True:

        strategy_5m = Strategy(indicator, macd_5m, bands_1dev, bands_2dev, volume_5m, rsi_5m, ema_12p, new_order)

        i = 1
        k = -2

        new_trade = Trade()

        params: dict

        while i < len(indicator.close_array):

            strategy_5m.strategy(i)

            if position.get_position() is False:

                if new_order.get_bottom():

                    params = {
                        "id": i,
                        "size": capital / indicator.candles[k][4],
                        "product_id": token,
                        "side": "buy",
                        "funds": capital,
                        "status": "done",
                        "done_at": indicator.date_array[i],
                        "executed_value": indicator.close_array[i]
                    }

                    writer = open("txt_files/data.txt", "w")
                    new_order.details = params
                    for line in new_order.details:
                        writer.write(str(new_order.details[line]) + "\n")
                    writer.close()

                    print("buy order details: ", new_order.details)

                    if "side" in new_order.details:
                        if new_order.get_key("side") == "buy":
                            position.long_position = True

                    #print("position: ", position.get_position())

                else:
                    new_order.is_bottom = False
                    new_order.is_raising = False
                    new_order.is_raising = False
                    new_order.is_top = False

            elif position.get_position():

                if new_order.get_top():

                    reader = open("txt_files/data.txt", "r")
                    reader.read()

                    params = {
                        "id": i,
                        "size": new_order.get_key("size"),
                        "product_id": token,
                        "side": "sell",
                        "funds": indicator.close_array[i] * new_order.get_key("size"),
                        "status": "done",
                        "done_at": indicator.date_array[i],
                        "executed_value": indicator.close_array[i]
                    }

                    new_order.details = params

                    if "side" in new_order.details:
                        if new_order.get_key("side") == "sell":
                            position.long_position = False

                    print("sell order details: ", new_order.details)
                    #print("position: ", position.get_position())

                    capital = indicator.close_array[i] * new_order.get_key("size")

                else:
                    new_order.is_bottom = False
                    new_order.is_raising = False
                    new_order.is_raising = False
                    new_order.is_top = False

            i = i + 1
            k = k - 1

            strategy_5m.index = 0

        lapse = indicator.date_array[-1] - indicator.date_array[0]

        if lapse >= 86400:

            lapse = lapse / 86400

        awriter = open("txt_files/capital_1.txt", "a")
        awriter.write(token + " capital: " + str(capital) + " in " + str(lapse) + "days" + "\n")

    print(capital)







