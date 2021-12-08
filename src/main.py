from flask import Flask, request, abort, render_template, redirect, url_for
from open_position import OpenPosition
from order import Order
from capital import Capital
from cbpro import AuthenticatedClient
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
from strategies import Strategy
import time
import Data

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def application():

    if request.method == 'POST':

        new_request = request.get_json(force=True)
        new_ticker = get_ticker(new_request)

        private_client = AuthenticatedClient(Data.API_Public_Key, Data.API_Secret_Key, Data.Passphrase)

        new_order = Order(private_client)
        position = OpenPosition(new_order)
        funds = Capital(private_client)

        indicator = Indicator()
        macd = MACD()

        candle_ticker: str
        stop_time: int
        candle_gra = int

        if position.get_position() and last_instance():

            candle_ticker = new_order.get_key("product_id")
            stop_time = get_time(27976)
            candle_gra = 300

            writer = open(Data.Time, "w")
            writer.write(str(time.time() + 5.0))
            writer.close()

        elif position.get_position() is False:

            candle_ticker = new_ticker
            stop_time = get_time(83925)
            candle_gra = 900

        try:
            indicator.set_candles(product=candle_ticker, callback=stop_time, begin=get_time(0), granularity=candle_gra)
        except ValueError as ve:
            print(ve.with_traceback())
        except NameError as ne:
            print(ne.with_traceback())

        indicator_list = [indicator, macd]
        try:
            for value in indicator_list:
                value.candles = indicator.candles
                value.set_indicator()
                value.set_dates()
        except Exception as e:
            print(e.with_traceback())

        indicator_5m = Indicator()
        macd_5m = MACD()

        if position.get_position() is False:

            if macd.hist[-1] > macd.hist[-2]:
                try:
                    indicator_5m.set_candles(product=new_ticker, callback=get_time(27976), begin=get_time(0),
                                             granularity=900)
                except ValueError as ve:
                    print(ve.with_traceback())
        else:
            indicator_5m = indicator
            macd_5m = macd

        volume_5m = VolSMA(timeperiod=20)
        bands2dev_5m = BB()
        bands1dev_5m = BB(ndbevup=1, nbdevdn=1)
        rsi_5m = RSI()
        ema_5m = EMA()
        momentum_5m = Momentum()

        indicators = [indicator_5m, macd_5m, volume_5m, bands1dev_5m, bands2dev_5m, rsi_5m, ema_5m, momentum_5m]

        try:
            for value in indicators:
                value.candles = indicator_5m.candles
                value.set_indicator()
                value.set_dates()
        except Exception as e:
            print(e.with_traceback())

        strategy_5m = Strategy(indicator_5m, macd_5m, bands1dev_5m, bands2dev_5m, volume_5m, rsi_5m, ema_5m, new_order)

        try:
            strategy_5m.strategy(-1)
        except Exception as e:
            print(e.with_traceback())

        trade_side: str
        trade_product: str
        trade_funds: str

        if (new_order.is_bottom()) and (position.get_position() is False):
            trade_side = "buy"
            trade_product = new_ticker
            trade_funds = funds.get_capital()
        elif (new_order.is_top()) and (position.get_position()):
            trade_side = "sell"
            trade_product = new_order.get_key("product_id")
            trade_funds = get_size(trade_product, new_order.get_key("filled_size"))

        try:
            print(trade_side + ", " + trade_funds + ", " + trade_side)
            
        except NameError as ne:
            print(ne.with_traceback())
        except KeyError as ke:
            print(ke.with_traceback())

        return 'success', 200

    elif request.method == 'GET':
        return redirect('http://3.218.228.129/login')

    else:
        abort(400)


@app.route("/login", methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            private_client = AuthenticatedClient(Data.API_Public_Key, Data.API_Secret_Key, Data.Passphrase)
            new_order = Order(private_client)
            return new_order.get_details()
    return render_template('login.html', error=error)

