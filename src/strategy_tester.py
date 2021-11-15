from open_position import OpenPosition
from order import Order
from cbpro import AuthenticatedClient
from indicators import Indicator
from indicators import RSI
from indicators import BB
from dict import new_dict
from trade import Trade
from new_strategies import MACDStrategy
from new_strategies import RSISTrategy
from new_strategies import Bollinger
import Data
import csv


#Body of script
#token = "AGLD-USD"
write = open("../../test_cases/bollinger_1dev_5m_test.txt", "w")
write.write("Buy when price less than lower band, sell when price greater than upper band\n")
write.write("token, capital, lapse, all_trades, prof_trades, success rate\n")
write.close()

for token in new_dict:
    new_reader = None
    try:
        data = open(f"../../data_5m/{token}_5m.csv", "r")
        new_reader = csv.reader(data)
    except FileNotFoundError as fnfe:
        continue

    listener = open("../txt_files/data.txt", "w")
    listener.close()

    candles = []
    for line in new_reader:
        candles.append(line)

    capital = 100
    private_client = AuthenticatedClient(Data.API_Public_Key, Data.API_Secret_Key, Data.Passphrase)
    new_order = Order(private_client)
    position = OpenPosition(new_order)
    indicator = Indicator()
    bands_1dev = BB(ndbevup=1, nbdevdn=1)

    indicator_list = [indicator, bands_1dev]
    for new_indicator in indicator_list:
        new_indicator.candles = candles[1:]
        new_indicator.get_data_set()
        new_indicator.reverse_data()
        new_indicator.get_dates()
        new_indicator.get_np_array()
        new_indicator.set_indicator()

    # verifies that the data and dates was extracted successfully
    h = 0
    y = -1
    while h < len(indicator.candles):
        if indicator.date_array[h] == indicator.candles[y][0]:
            pass
        else:
            raise ValueError("dates do not match")
        if indicator.close_array[h] == float(indicator.candles[y][4]):
            pass
        else:
            raise ValueError("close prices do not match")
        h = h + 1
        y = y - 1

    if token in new_dict:
        strategy_5m = Bollinger(indicator, bands_1dev, new_order)
        new_trade = Trade()
        params: dict
        all_trades = 0
        prof_trades = 0
        success_rate = 0
        i = 1
        k = -2

        while i < len(indicator.close_array):
            strategy_5m.strategy(index=i, beg=k)
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

            elif position.get_position():

                ready_to_trade = False
                avg_cost = float(new_order.get_key("executed_value")) / float(new_order.get_key("size"))
                percentage = ((float(indicator.get_index(-1) * 100)) / avg_cost) - 100

                if new_order.is_top:
                    ready_to_trade = True
                    done_reason = strategy_5m.index

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

            i = i + 1
            k = k - 1
            strategy_5m.reset_order()
            strategy_5m.index = 0

        lapse = float(indicator.date_array[-1]) - float(indicator.date_array[0])
        if lapse >= 86400:
            lapse = lapse / 86400
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

        awriter = open("../../test_cases/bollinger_1dev_5m_test.txt", "a")
        for key in final:
            awriter.write(f"{final[key]}, ")
        awriter.write("\n")
        awriter.close()
        print(capital)