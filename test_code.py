from cbpro import AuthenticatedClient
from cbpro import PublicClient
from datetime import datetime
from indicators import Indicator
from indicators import MACD
from indicators import BB
from indicators import RSI
from indicators import VolSMA
from indicators import EMA
from app_methods import get_time
from app_methods import last_instance
from app_methods import get_size
from app_methods import get_unix
from open_position import OpenPosition
from order import Order
from capital import Capital
from strategies import Strategy
import time
import pytz
import Data


def app(ticker="", a_time=0, index=int):

    new_ticker = ticker

    _time = a_time
    tz = pytz.timezone('US/Eastern')
    finish = datetime.fromtimestamp(_time, tz).isoformat()
    start = datetime.fromtimestamp(_time - 27976, tz).isoformat()

    client = AuthenticatedClient(Data.API_Public_Key, Data.API_Secret_Key, Data.Passphrase)

    new_order = Order(client)
    new_order.get_id()
    new_order.set_details()

    position = OpenPosition(new_order)
    position.set_position()

    funds = Capital(client)
    funds.set_capital()

    p_client = PublicClient()
    indicator = Indicator()
    indicator.initiate_client(p_client)

    successful_analysis = False

    if position.get_position() and last_instance():

        try:
            indicator.set_candles(product=new_order.get_key("product_id"), callback=get_time(27976), begin=get_time(0),
                                  granularity=300)

        except ValueError:
            print(new_ticker)
            print(indicator.candles)
            # wait to make another request
            pass

        writer = open(Data.Time, "w")
        writer.write(str(time.time()))
        writer.close()

    else:

        try:
            indicator.set_candles(product=new_ticker, callback=start, begin=finish, granularity=300)

        except ValueError:
            print(new_ticker)
            print(indicator.candles)
            # wait to make another request
            pass

    macd_5m = MACD()
    volume_5m = VolSMA(timeperiod=20)
    bands_2dev = BB()
    bands_1dev = BB(ndbevup=1, nbdevdn=1)
    rsi_5m = RSI()
    ema_12p = EMA()

    if len(indicator.candles) > 0:

        try:
            indicator.get_data_set()
            indicator.reverse_data()
            indicator.get_np_array()
        except Exception:
            print("indicators failed for: " + new_ticker)
            print(indicator.candles)

        try:
            macd_5m.np_array = indicator.np_array
            macd_5m.get_MACD()
        except Exception:
            print("macd failed for: " + new_ticker)
            print(indicator.candles)

        try:
            bands_2dev.np_array = indicator.np_array
            bands_2dev.get_BB()
        except Exception:
            print("bands_2dev failed for: " + new_ticker)
            print(indicator.candles)

        try:
            bands_1dev.np_array = indicator.np_array
            bands_1dev.get_BB()
        except Exception:
            print("bands_1dev failed for: " + new_ticker)
            print(indicator.candles)

        try:
            rsi_5m.np_array = indicator.np_array
            rsi_5m.get_RSI()
        except Exception:
            print("rsi failed for: " + new_ticker)
            print(indicator.candles)

        try:
            ema_12p.np_array = indicator.np_array
            ema_12p.get_EMA()
        except Exception:
            print("ema_12 failed for: " + new_ticker)
            print(indicator.candles)

        try:
            volume_5m.candles = indicator.candles
            volume_5m.get_data_set()
            volume_5m.reverse_data()
            volume_5m.get_np_array()
            volume_5m.get_volume()
        except Exception:
            print("volume_ema failed for: " + new_ticker)
            print(indicator.candles)
            print(ema_12p.real)

    else:
        # try setting candles again
        pass

    if len(volume_5m.real) > 0:

        strategy_5m = Strategy(indicator, macd_5m, bands_1dev, bands_2dev, volume_5m, rsi_5m, ema_12p, new_order)
        strategy_5m.strategy(index)


        successful_analysis = True

    else:
        # Means that the indicators could not be measured
        pass

    # If there is no a position opened it will trigger a buy order
    if position.get_position() is False:

        if successful_analysis:

            # Rules to make ready_to_trade True
            if strategy_5m.order.get_bottom() and not strategy_5m.order.get_top () and not strategy_5m.order.get_fall():
                print(new_ticker + ": " + str(strategy_5m.order.is_bottom) + ", " + str(strategy_5m.order.is_raising) + ", " + str(strategy_5m.order.is_top) + ", " + str(strategy_5m.order.is_falling))
                ready_to_trade = True
                print("ready to trade:", ready_to_trade)
            else:
                print(new_ticker + ": " + str(strategy_5m.order.is_bottom) + ", " + str(strategy_5m.order.is_raising) + ", " + str(strategy_5m.order.is_top) + ", " + str(strategy_5m.order.is_falling))
                ready_to_trade = False

            if strategy_5m.order.is_falling and not strategy_5m.order.is_bottom and not strategy_5m.order.is_raising:
                ready_to_sell = True
                print(new_ticker + ": " + str(strategy_5m.order.is_bottom) + ", " + str(strategy_5m.order.is_raising) + ", " + str(strategy_5m.order.is_top) + ", " + str(strategy_5m.order.is_falling))
                print("ready to sell:", ready_to_sell)
            else:
                print(new_ticker + ": " + str(strategy_5m.order.is_bottom) + ", " + str(strategy_5m.order.is_raising) + ", " + str(strategy_5m.order.is_top) + ", " + str(strategy_5m.order.is_falling))
                ready_to_sell = False

        else:
            pass

    # If there is a long position but the ticker is not the same as the order's
    # the program will just ignore it
    else:
        pass


new_app = app("BOND-USD", 1629053842, -1)

