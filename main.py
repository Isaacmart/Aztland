from flask import Flask, request, abort, render_template
from open_position import OpenPosition
from order import Order
from capital import Capital
from cbpro.authenticated_client import AuthenticatedClient
from indicators import *
from app_methods import *
import Data

app = Flask(__name__)

key = Data.API_Public_Key
b64secret = Data.API_Secret_Key
passphrase = Data.Passphrase

client = AuthenticatedClient(key, b64secret, passphrase)
pclient = PublicClient()
new_order = Order(client)
new_order.get_id()
new_order.set_details()
position = OpenPosition(new_order)
position.set_position()
funds = Capital(client)
funds.set_capital()


@app.route("/", methods=['GET', 'POST'])
def application():
    if request.method == 'POST':
        new_request = request.get_json(force=True)

        # If there is no a position opened it will trigger a buy order
        if position.get_position() is False:

            if float(new_request['hist']) > 0:
                indicator = Indicator(client=pclient)
                indicator.set_candles(product=get_key('ticker', new_request), callback=get_time(27976),
                                      begin=get_time(0),
                                      granularity=300)
                indicator.get_data_set()
                indicator.reverse_data()
                indicator.get_np_array()
                macd_5m = MACD(client=pclient)
                macd_5m.np_array = indicator.np_array
                macd_5m.get_MACD()
                volume_5m = VolSMA(client=pclient, timeperiod=20)
                volume_5m.candles = indicator.candles
                volume_5m.get_data_set()
                volume_5m.reverse_data()
                volume_5m.get_np_array()
                volume_5m.get_volume()

                # Buy if True
                if (macd_5m.hist[-1] > 0 and volume_5m.data_array[-1] > volume_5m.real[-1]) or (macd_5m.hist[-2] >= macd_5m.hist[-3]):

                    new_trade = client.place_market_order(product_id=get_key('ticker', new_request),
                                                          side="buy",
                                                          funds=funds.get_capital())

                    if "id" in new_trade:
                        writer = open("/var/www/jdsdkf.xyz/html/CryptoTrader/data.txt", "w")
                        writer.write(new_trade['id'])
                        writer.close()
                        new_order.get_id()

                    else:
                        print("order cannot be completed")

                    if new_order.set_details():
                        position.set_position()
                        print("order sent " + new_order.get_key('product_id') + " " + new_order.get_key('funds'))

                    else:
                        print("opening position details: ", new_trade)

                else:
                    # Does nothing if both statements are False
                    print("requirements were not met for ", get_key('ticker', new_request))

            else:
                print("position: ", position.order.details)

        # If the Post request ticker is the same as the order's it will trigger a sell order
        elif position.get_position() and get_key('ticker', new_request) == new_order.get_key('product_id'):

            # Sell if True
            if float(new_request['hist']) < 0.0:
                new_trade = client.place_market_order(product_id=new_order.get_key("product_id"),
                                                      side='sell',
                                                      size=new_order.get_key('filled_size'))

                if "id" in new_trade:
                    writer = open("/var/www/jdsdkf.xyz/html/CryptoTrader/data.txt", "w")
                    writer.write(new_trade['id'])
                    writer.close()
                    new_order.get_id()

                if new_order.set_details():
                    print("order sent " + new_order.get_key('product_id') + " " + new_order.get_key('funds'))
                    funds.capital = float(new_order.get_key('executed_value'))
                    position.set_position()

                else:
                    print("order details", new_trade)
            else:
                print("coin is not ready to be sold")

        elif position.get_position() and get_key('ticker', new_request) != new_order.get_key('product_id'):

            print(get_key('ticker', new_request), "ticker does not match the product id from order",
                  new_order.get_key('product_id'))

        # If there is a long position but the ticker is not the same as the order's
        # the program will just ignore it
        else:
            print("Nothing to do", get_key('ticker', new_request))

        return 'success', 200

    elif request.method == 'GET':
        return render_template('index.html')

    else:
        abort(400)






