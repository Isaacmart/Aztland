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
from strategies import Strategy
import time
import Data

app = Flask(__name__)

#This is the debug mode of the actual application that will execute trades automatically, hence why it is printing
#to stdio. It does it so that way the print statements can be accessed in the error log
#The actual application will store all the logs errors.


@app.route("/", methods=['GET', 'POST'])
def application():

    if request.method == 'POST':
        new_request = request.get_json(force=True)
        new_ticker = get_ticker('ticker', new_request)

        client = PublicClient()
        private_client = AuthenticatedClient(Data.API_Public_Key, Data.API_Secret_Key, Data.Passphrase)

        new_order = Order(private_client)
        if len(new_order.get_id()) > 0:
            new_order.set_details()
        else:
            print("unable to get Id number")
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
                indicator.set_candles(product=new_order.get_key("product_id"), callback=get_time(27976),
                                      begin=get_time(0),
                                      granularity=300)
                print("candles set", new_order.get_key("product_id"))
            except ValueError as ve:
                print(new_ticker, ve)
            writer = open(Data.Time, "w")
            writer.write(str(time.time()))
            writer.close()
        elif position.get_position() is False:
            try:
                indicator.set_candles(product=new_ticker, callback=get_time(27976), begin=get_time(0), granularity=300)
            except ValueError as ve:
                print(new_ticker, ve)
        else:
            pass

        invalid_data = False
        for value in indicator.candles:
            if value.__class__ is None:
                invalid_data = True
                break

        indicator_values = []
        if invalid_data is False:
            indicator_list = [indicator, macd_5m, volume_5m, bands_2dev, bands_1dev, rsi_5m, ema_12p, momentum]
            try:
                for a_indicator in indicator_list:
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
                print(indicator.candles)

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

            if position.get_position() is False:
                if new_order.is_bottom:
                    new_trade = private_client.place_market_order(product_id=new_ticker, side="buy",
                                                                  funds=funds.get_capital())
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
                        print(new_ticker, new_trade)
                        pass
                else:
                    pass
            elif position.get_position():

                done_reason = 0
                ready_to_trade = False
                avg_cost = float(new_order.get_key("executed_value")) / float(new_order.get_key("filled_size"))
                percentage = ((float(indicator.get_index(-1) * 100)) / avg_cost) - 100
                if new_order.is_top:
                    ready_to_trade = True
                    done_reason = 1
                elif percentage >= 10.0 and not new_order.is_raising:
                    ready_to_trade = True
                    done_reason = 2
                else:
                    pass

                if ready_to_trade:
                    new_trade = private_client.place_market_order(product_id=new_order.get_key("product_id"),
                                                                  side='sell',
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
                        print("order details", done_reason, new_trade)
                else:
                    pass
        else:
            pass
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
            new_order.get_id()
            new_data = new_order.details
            return new_data
    return render_template('login.html', error=error)
