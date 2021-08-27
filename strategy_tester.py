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

    while index < 1:

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

    if successful_exec is True:

        strategy_5m = Strategy(indicator, macd_5m, bands_1dev, bands_2dev, volume_5m, rsi_5m, ema_12p, new_order)

        i = 0

        new_trade = Trade()

        params: dict

        while i < 1:

            strategy_5m.strategy(i)

            print(position.get_position())

            if position.get_position() is False:

                if new_order.get_bottom():

                    params = {
                        "id": i,
                        "size": capital / indicator.candles[i][4],
                        "product_id": token,
                        "side": "buy",
                        "funds": capital,
                        "status": "done",
                        "executed_value": indicator.candles[i][4]
                    }

                    new_trade.b_size = capital / indicator.candles[i][4]
                    new_trade.buy_price = indicator.candles[i][4]

                    new_order.details = params
                    print(new_order.details)
                    new_order.set_details()

            elif position.get_position():

                if new_order.get_top():

                    params = {
                        "id": i,
                        "product_id": token,
                        "size": new_order.details["size"],
                        "side": "sell",
                        "funds": indicator.candles[i][4],
                        "status": "done",
                        "executed_value": indicator.candles[i][4]
                    }

                    new_trade.s_size = new_order.details["size"]
                    new_trade.sell_price = indicator.candles[i][4]

                    new_order.details = params
                    new_order.set_details()

                    capital = (new_trade.s_size * new_trade.sell_price)
                    print(new_trade.buy_price + " " + new_trade.sell_price + " \n")

            i = i + 1

            strategy_5m.index = 0

    print(capital)







