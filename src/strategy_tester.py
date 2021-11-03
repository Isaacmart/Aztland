from flask import Flask, request, abort, render_template, redirect, url_for
from open_position import OpenPosition
from order import Order
from capital import Capital
from cbpro import AuthenticatedClient
from cbpro import PublicClient
from indicators import Indicator
from indicators import MACD
from indicators import BB
from indicators import RSI
from indicators import VolSMA
from indicators import EMA
from indicators import Momentum
from app_methods import get_time
from app_methods import get_ticker
from app_methods import last_instance
from app_methods import get_size
from dict import new_dict
from strategies import Strategy
from trade import Trade
import time
import Data
import csv

#token = "AGLD-USD"
for token in new_dict:
    try:
        data = open(f"../../data_5m/{token}_5m.csv", "r")
    except FileNotFoundError as new_fnfe:
        continue

    new_reader = csv.reader(data)
    candles = []
    for line in new_reader:
        candles.append(line)

    capital = 100
    private_client = AuthenticatedClient(Data.API_Public_Key, Data.API_Secret_Key, Data.Passphrase)
    new_order = Order(private_client)
    position = OpenPosition(new_order)
    indicator = Indicator()
    macd_5m = MACD()
    bands_1dev = BB(ndbevup=1, nbdevdn=1)
    bands_2dev = BB()
    volume_5m = VolSMA(timeperiod=20)
    rsi_5m = RSI()
    ema_12p = EMA()
    momentum = Momentum()

    indicator.candles = candles[1:]
    indicator.get_data_set()
    indicator.reverse_data()
    indicator.get_dates()
    indicator.get_np_array()

    indicator_list = [macd_5m, volume_5m, bands_2dev, bands_1dev, rsi_5m, ema_12p, momentum]
    for new_indicator in indicator_list:
        new_indicator.candles = candles[1:]
        new_indicator.get_data_set()
        new_indicator.reverse_data()
        new_indicator.get_dates()
        new_indicator.get_np_array()
        new_indicator.set_indicator()
        # print(new_indicator.get_index(-1))

    # verifies that the data was extracted successfully
    h = 0
    y = -1
    while h < 3:
        if indicator.date_array[h] == indicator.candles[y][0]:
            pass
        else:
            raise ValueError("dates do not match")

        h = h + 1
        y = y - 1

    #Verifies that the dates were extracted successfully
    l = 0
    q = -1
    while l < len(indicator.candles):
        if indicator.close_array[l] == float(indicator.candles[q][4]):
            pass
        else:
            raise ValueError("close prices do not match")
        l = l + 1
        q = q - 1

    if True:
        strategy_5m = Strategy(indicator, macd_5m, bands_1dev, bands_2dev, volume_5m, rsi_5m, ema_12p, new_order)
        i = 1
        k = -2
        new_trade = Trade()
        params: dict
        all_trades = 0
        prof_trades = 0
        while i < len(indicator.close_array):
            strategy_5m.strategy(i, beg=k)
            if position.get_position() is False:
                if new_order.get_bottom():
                    params = {
                        "id": i,
                        "size": capital / float(indicator.candles[k][4]),
                        "product_id": token,
                        "side": "buy",
                        "funds": capital,
                        "status": "done",
                        "done_at": indicator.date_array[i],
                        "executed_value": capital * 0.995,
                        "product_price": indicator.close_array[i]
                    }
                    writer = open("../txt_files/data.txt", "w")
                    new_order.details = params
                    for line in new_order.details:
                        writer.write(str(new_order.details[line]) + "\n")
                    writer.close()
                    print("buy order details: ", new_order.details)
                    if "side" in new_order.details:
                        if new_order.get_key("side") == "buy":
                            position.long_position = True
                    # print("position: ", position.get_position())

                new_order.is_bottom = False
                new_order.is_raising = False
                new_order.is_raising = False
                new_order.is_top = False

            elif position.get_position():

                ready_to_trade = False
                avg_cost = float(new_order.get_key("executed_value")) / float(new_order.get_key("size"))
                percentage = ((float(indicator.get_index(-1) * 100)) / avg_cost) - 100

                if new_order.is_top:
                    ready_to_trade = True
                    done_reason = 1
                elif percentage >= 10.0 and not new_order.is_raising:
                    ready_to_trade = True
                    done_reason = 2
                elif percentage >= 5.0 and new_order.is_falling:
                    ready_to_trade = True
                    done_reason = 3
                elif percentage <= -5.0 and not new_order.is_raising:
                    ready_to_trade = True
                    done_reason = 4
                elif percentage <= -10.0 and not new_order.is_raising:
                    ready_to_trade = True
                    done_reason = 5
                else:
                    pass

                if ready_to_trade:
                    reader = open("../txt_files/data.txt", "r")
                    reader.read()
                    new_size = new_order.get_key("size")
                    capital = (indicator.close_array[i] * new_size) * 0.995

                    if capital > new_order.get_key("executed_value"):
                        all_trades = all_trades + 1
                        prof_trades = prof_trades + 1
                    else:
                        all_trades = all_trades + 1

                    params = {
                        "id": i,
                        "size": new_size,
                        "product_id": token,
                        "side": "sell",
                        "funds": indicator.close_array[i] * new_size,
                        "status": "done",
                        "done_at": indicator.date_array[i],
                        "executed_value": capital,
                        "product_price": indicator.close_array[i]
                    }

                    new_order.details = params
                    if "side" in new_order.details:
                        if new_order.get_key("side") == "sell":
                            position.long_position = False
                    print("sell order details: ", new_order.details)
                    # print("position: ", position.get_position())

                new_order.is_bottom = False
                new_order.is_raising = False
                new_order.is_raising = False
                new_order.is_top = False
            i = i + 1
            k = k - 1
            strategy_5m.index = 0

        lapse = float(indicator.date_array[-1]) - float(indicator.date_array[0])
        if lapse >= 86400:
            lapse = lapse / 86400
        success_rate = 0
        try:
            success_rate = (prof_trades * 100) / all_trades
        except ZeroDivisionError:
            print(new_order.details)

        final = {
            "token": token,
            "capital": "%.2f" % capital,
            "days": "%.2f" % lapse,
            "all_trades": all_trades,
            "success_trades": prof_trades,
            "success_rate": "%.2f" % success_rate
        }

        awriter = open("../../test_cases/test_03.txt", "a")
        new_str = "token, capital, lapse, all_trades, prof_trades, success rate"
        awriter.write(
            token + ", " + str("%.2f" % capital) + ", " + str("%.2f" % lapse) + ", " + str(all_trades) + ", " + str(
                prof_trades) + ", " + str("%.2f" % success_rate) + "\n")
        awriter.close()

        print(capital)