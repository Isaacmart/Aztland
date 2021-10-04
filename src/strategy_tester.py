from strategies import Strategy
from cbpro import PublicClient
from cbpro import AuthenticatedClient
from order import Order
from open_position import OpenPosition
from dict import new_dict
from capital import Capital
from indicators import Indicator
from indicators import MACD
from indicators import VolSMA
from indicators import BB
from indicators import RSI
from indicators import EMA
from indicators import Momentum
from trade import Trade
from app_methods import get_time
from app_methods import get_ticker
from app_methods import last_instance
from app_methods import get_size
from strategies import Strategy
import Data
import time
import csv

new_request: dict

client = PublicClient()
private_client = AuthenticatedClient(Data.API_Public_Key, Data.API_Secret_Key, Data.Passphrase)
new_ticker = "FARM-USD"

new_order = Order(private_client)
new_order.get_id()
new_order.set_details()
position = OpenPosition(new_order)
position.set_position()
funds = Capital(private_client)
funds.set_capital()

indicator = Indicator()
macd_5m = MACD()
volume_5m = VolSMA(timeperiod=20)
bands_2dev = BB()
bands_1dev = BB(ndbevup=1, nbdevdn=1)
rsi_5m = RSI()
ema_12p = EMA()
momentum = Momentum()

indicator.initiate_client(client)
if position.get_position() and last_instance():
    try:
        indicator.set_candles(product=new_order.get_key("product_id"), callback=get_time(27976), begin=get_time(0),
                              granularity=300)
    except ValueError as ve:
        print(new_ticker, indicator.candles)
    writer = open(Data.Time, "w")
    writer.write(str(time.time()))
    writer.close()
elif position.get_position() is False:
    try:
        indicator.set_candles(product=new_ticker, callback=get_time(27976), begin=get_time(0), granularity=300)
    except ValueError as ve:
        print(new_ticker, indicator.candles)
indicator.get_data_set()
indicator.reverse_data()
indicator.get_dates()
indicator.get_np_array()

indicatorList = [macd_5m, volume_5m, bands_2dev, bands_1dev, rsi_5m, ema_12p, momentum]
indicator_values = []

try:
    for a_indicator in indicatorList:
        a_indicator.candles = indicator.candles
        a_indicator.get_data_set()
        a_indicator.reverse_data()
        a_indicator.get_dates()
        a_indicator.get_np_array()
        a_indicator.set_indicator()
        if a_indicator.get_index(-1).__class__ == list:
            for value in a_indicator.get_index(-1):
                indicator_values.append(value)
        else:
            indicator_values.append(a_indicator.get_index(-1))
except Exception as e:
    print(e.__class__)


passed = False
for value in indicator_values:
    if value.__class__ == float:
        passed = True
    else:
        passed = False
        break

if passed:
    strategy_5m = Strategy(indicator, macd_5m, bands_1dev, bands_2dev, volume_5m, rsi_5m, ema_12p, new_order)
    strategy_5m.strategy(-1)
else:
    exit(0)

if position.get_position() is False:
    if new_order.is_bottom:
        new_trade = private_client.place_market_order(product_id=new_ticker, side="buy", funds=funds.get_capital())
        if "id" in new_trade:
            writer = open(Data.Path, "w")
            writer.write(new_trade['id'])
            writer.close()
            new_order.get_id()
            if new_order.set_details():
                writer = open(Data.Time, "w")
                writer.write(str(time.time()))
                writer.close()
                print("order sent: ", new_order.details)
            else:
                print("opening position details: ", new_trade)
        else:
            print(new_ticker + " " + str(new_trade))
            pass
    else:
        exit(0)
elif position.get_position():
    if new_order.is_top:
        new_trade = private_client.place_market_order(product_id=new_order.get_key("product_id"), side='sell',
                                              size=get_size(new_order.get_key("product_id"),
                                                            new_order.get_key('filled_size')))
        if "id" in new_trade:
            writer = open(Data.Path, "w")
            writer.write(new_trade['id'])
            writer.close()
            new_order.get_id()
            if new_order.set_details():
                print("order sent " + new_order.get_key('product_id'))
            else:
                pass
        else:
            print("order details", new_trade)
    else:
        exit(0)

if passed:
    strategy_5m = Strategy(indicator, macd_5m, bands_1dev, bands_2dev, volume_5m, rsi_5m, ema_12p, new_order)
    strategy_5m.strategy(-1)
    print(strategy_5m.index)
    print(strategy_5m.order.is_top)
    print(strategy_5m.order.is_raising)
    print(strategy_5m.order.is_bottom)
    print(strategy_5m.order.is_falling)
