from flask import Flask, request, abort, render_template
from open_position import OpenPosition
from order import Order
from capital import Capital
from cbpro.authenticated_client import AuthenticatedClient
from dict import new_dict
from indicators import *
from app_methods import *
import Data

app = Flask(__name__)

key = Data.API_Public_Key
b64secret = Data.API_Secret_Key
passphrase = Data.Passphrase


@app.route("/", methods=['GET', 'POST'])
def application():
    if request.method == 'POST':

        new_request = request.get_json(force=True)

        client = AuthenticatedClient(key, b64secret, passphrase)
        pclient = PublicClient()
        new_order = Order(client)
        new_order.get_id()
        new_order.set_details()
        position = OpenPosition(new_order)
        position.set_position()
        funds = Capital(client)
        funds.set_capital()

        new_ticker = get_key('ticker', new_request)

        # If there is no a position opened it will trigger a buy order
        if position.get_position() is False:

            if float(new_request['hist']) > 0:

                indicator = Indicator(client=pclient)
                indicator.set_candles(product=new_ticker, callback=get_time(27976), begin=get_time(0),
                                      granularity=300)
                macd_5m = MACD(client=pclient)
                volume_5m = VolSMA(client=pclient, timeperiod=20)
                bands_5m = BB(client=pclient)

                try:
                    indicator.get_data_set()
                    indicator.reverse_data()
                    indicator.get_np_array()

                    macd_5m.np_array = indicator.np_array
                    macd_5m.get_MACD()

                    bands_5m.np_array = indicator.np_array
                    bands_5m.get_BB()

                    volume_5m.candles = indicator.candles
                    volume_5m.get_data_set()
                    volume_5m.reverse_data()
                    volume_5m.get_np_array()
                    volume_5m.get_volume()

                except Exception as e:
                    print("talib failed", indicator.candles[-1])
                    pass

                ready_to_trade = None

                # Rules to make ready_to_trade True
                if ((macd_5m.hist[-1] and macd_5m.hist[-2]) > 0) and (macd_5m.macd[-1] > macd_5m.macd[-2]) and \
                        (volume_5m.data_array[-1] < volume_5m.real[-1]):

                    ready_to_trade = True

                elif ((macd_5m.macd[-1] and macd_5m.signal[-1]) < 0) and (macd_5m.hist[-1] > 0) and \
                        (bands_5m.middleband[-1] > bands_5m.middleband[-2]):

                    ready_to_trade = True

                elif (indicator.data_array[-1] > indicator.data_array[-2]) and (volume_5m.real[-2] < volume_5m[-1]):

                    ready_to_trade = True

                # Rules that will make ready_to_trade false again
                if (indicator.data_array[-1] > (bands_5m.upperband[-1] or bands_5m.middleband[-1])) and \
                        (indicator.data_array[-1] < bands_5m.middleband[-1]):

                    ready_to_trade = False

                #Will trigger a buy order if a rule is True
                if ready_to_trade is True:

                    new_trade = client.place_market_order(product_id=new_ticker, side="buy", funds=funds.get_capital())

                    if "id" in new_trade:
                        writer = open(Data.Path, "w")
                        writer.write(new_trade['id'])
                        writer.close()
                        new_order.get_id()

                        if new_order.set_details():
                            position.set_position()
                            print("order sent: ", new_order.details)

                        else:
                            print("opening position details: ", new_trade)

                    else:
                        print("order cannot be completed for: ", new_ticker, new_trade)

                else:
                    # Does nothing if both statements are False
                    print("requirements were not met for ", new_ticker + " " + str(macd_5m.hist[-1])
                          + " " + str(macd_5m.hist[-2]) + " " + str(volume_5m.real[-1]) + ' ' +
                          str(volume_5m.data_array[-1]))

            else:
                print("request- ", new_request["ticker"] + ", " + new_request['hist'])

        # If the Post request ticker is the same as the order's it will trigger a sell order
        elif position.get_position():

            ready_to_trade = False

            indicator = Indicator(client=pclient)
            indicator.set_candles(product=new_ticker, callback=get_time(27976), begin=get_time(0), granularity=300)

            macd_5m = MACD(client=pclient)
            volume_5m = VolSMA(client=pclient, timeperiod=20)
            bands_5m = BB(indicator)

            try:
                indicator.get_data_set()
                indicator.reverse_data()
                indicator.get_np_array()

                macd_5m.np_array = indicator.np_array
                macd_5m.get_MACD()

                bands_5m.np_array = indicator.np_array
                bands_5m.get_BB()

                volume_5m.candles = indicator.candles
                volume_5m.get_data_set()
                volume_5m.reverse_data()
                volume_5m.get_np_array()
                volume_5m.get_volume()

            except Exception as e:
                print("talib failed", indicator.candles[-1])
                pass

            #rules for when the request ticker is the same as the position's
            if new_ticker == new_order.get_key("product_id"):

                if float(new_request['hist']) < 0.0:

                    ready_to_trade = True

            #rules for when the request ticker is other than the position's
            else:

                if (macd_5m.hist[-2] > macd_5m.hist[-1]) and (indicator.data_array[-1] < indicator.data_array[-2]) \
                        and (volume_5m.real[-2] > volume_5m.real[-1]):

                    ready_to_trade = True

                elif (indicator.data_array[-1] < bands_5m.middleband[-1]) and \
                        (indicator.data_array[-1] < indicator.data_array[-2]):

                    ready_to_trade = True

            #Triggers a sell order if a rule is met:
            if ready_to_trade:

                new_trade = client.place_market_order(product_id=new_order.get_key("product_id"), side='sell',
                                                      size=get_size(new_order.get_key("product_id"),
                                                                    new_order.get_key('filled_size')))

                if "id" in new_trade:
                    writer = open(Data.Path, "w")
                    writer.write(new_trade['id'])
                    writer.close()
                    new_order.get_id()

                    if new_order.set_details():
                        print("order sent " + new_order.get_key('product_id'))
                        funds.capital = float(new_order.get_key('executed_value'))
                        position.set_position()

                    else:
                        print("trade was not closed: ", new_trade)

                else:
                    print("order details", new_trade)

            #Not rules were true
            else:
                print("coin is not ready to be sold", new_order.get_key('product_id'))

        # If there is a long position but the ticker is not the same as the order's
        # the program will just ignore it
        else:
            print("Nothing to do", new_ticker)

        return 'success', 200

    elif request.method == 'GET':
        return render_template('index.html')

    else:
        abort(400)
