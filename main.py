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

        #ticker converted into a Coinbase product id
        new_ticker = get_key('ticker', new_request)

        indicator = Indicator(client=pclient)

        if position.get_position() is False:

            indicator.set_candles(product=new_ticker, callback=get_time(83929), begin=get_time(0), granularity=900)

        else:
            indicator.set_candles(product=new_order.get_key("product_id"), callback=get_time(83929), begin=get_time(0), granularity=900)

        macd_15m = MACD(client=pclient)
        volume_15m = VolSMA(client=pclient, timeperiod=20)
        bands_2dev = BB(client=pclient)
        bands_1dev = BB(client=pclient, ndbevup=1, nbdevdn=1)
        rsi_15m = RSI(client=pclient)
        ema_12p = EMA(client=pclient)

        try:
            indicator.get_data_set()
            indicator.reverse_data()
            indicator.get_np_array()

            macd_15m.np_array = indicator.np_array
            macd_15m.get_MACD()

            bands_2dev.np_array = indicator.np_array
            bands_2dev.get_BB()

            bands_1dev.np_array = indicator.np_array
            bands_1dev.get_BB()

            rsi_15m.np_array = indicator.np_array
            rsi_15m.get_RSI()

            ema_12p.np_array = indicator.np_array
            ema_12p.get_EMA()

            volume_15m.candles = indicator.candles
            volume_15m.get_data_set()
            volume_15m.reverse_data()
            volume_15m.get_np_array()
            volume_15m.get_volume()

        except Exception as e:
            print(e)
            pass

        #Asserts stock is at a bottom
        is_bottom: bool
        bottom_rule_used: str

        if (indicator.data_array[-2] < bands_2dev.lowerband[-2]) and (bands_2dev.lowerband[-1] < indicator.data_array[-1]) and (0 > macd_15m.hist[-1] > macd_15m.hist[-2]):
            is_bottom = False
            bottom_rule_used = "price < lowerband 2, hist increasing"

        elif (bands_2dev.lowerband[-2] < indicator.data_array[-2] < bands_1dev.lowerband[-2]) and (0 > macd_15m.macd[-1] > macd_15m.macd[-2]):
            is_bottom = True
            bottom_rule_used = "lowerband 2 < price < lowerband 1, macd increasing"

        elif (indicator.data_array[-2] < bands_1dev.lowerband[-2]) and (0 < macd_15m.hist[-2] < macd_15m.hist[-1]):
            is_bottom = True
            bottom_rule_used = "price < lowerband 1, macd hist increasing"

        elif (rsi_15m.real[-1] < 30) and (macd_15m.macd[-1] > macd_15m.macd[-2]):
            is_bottom = True
            bottom_rule_used = "rsi < 30, mcad increasing"

        elif rsi_15m.real[-2] < rsi_15m.real[-1] < 50:
            is_bottom = True
            bottom_rule_used = "rsi incresing but less than 50"

        else:
            is_bottom = False
            bottom_rule_used = "no at bottom"

        #Assert is a stock is raising
        is_raising: bool
        raising_rule: str

        if (indicator.data_array[-1] > bands_1dev.upperband[-1]) and (macd_15m.macd[-1] > macd_15m.macd[-1]):
            is_raising = True
            raising_rule = "price > uppperband 1, macd increasing"

        elif bands_1dev.upperband[-1] > indicator.data_array[-1] > indicator.data_array[-2] > ema_12p.real[-2]:
            is_raising = True
            raising_rule = "price > 12 ema"

        else:
            is_raising = False
            raising_rule = "no raising"

        #Assert if a stock is at the top
        is_top: bool
        top_rule: str

        if indicator.data_array[-1] > bands_2dev.upperband[-1]:
            is_top = True
            top_rule = "price > upperband 2"

        elif rsi_15m.real[-1] > 70:
            is_top = True
            top_rule = "rsi > 70"

        else:
            is_top = False
            top_rule = "Not at top"

        #Assert is stock is falling from top
        is_falling: bool
        falling_rule: str

        if (bands_1dev.upperband[-2] > indicator.data_array[-2] > bands_2dev.upperband[-2]) and (indicator.data_array[-1] < bands_1dev.upperband[-1]):
            is_falling = True
            falling_rule = "price crossing down upperband 1"

        elif (indicator.data_array[-2] > bands_2dev.upperband[-2]) and (indicator.data_array[-1] < bands_2dev.upperband[-1]):
            is_falling = True
            falling_rule = "price crossing down upperband 2"

        elif bands_1dev.upperband[-1] < indicator.data_array[-1] < bands_2dev.upperband[-1] < float(indicator.candles[0][3]):
            is_falling = True
            falling_rule = "close price < open price over upperband 1"

        else:
            is_falling = False
            falling_rule = "no falling"

        # If there is no a position opened it will trigger a buy order
        if position.get_position() is False:

            if float(new_request['hist']) > 0:

                ready_to_trade: bool

                # Rules to make ready_to_trade True
                if (is_bottom or is_raising) and ((is_top and is_falling) is False):

                    ready_to_trade = True

                else:
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
                            print("with: ")
                            print(top_rule)
                            print(bottom_rule_used)
                            print(raising_rule)
                            print(falling_rule)

                        else:
                            print("opening position details: ", new_trade)

                    else:
                        pass

                else:
                    # Does nothing if both statements are False
                    pass

            else:
                pass

        # If the Post request ticker is the same as the order's it will trigger a sell order
        elif position.get_position():

            ready_to_trade: bool

            #rules for when the request ticker is other than the position's:
            #rules for when the request ticker is the same as the position's
            #if (new_ticker == new_order.get_key("product_id")) and (float(new_request['hist']) < 0.0):
                #ready_to_trade = True

            if is_falling and is_bottom is False:
                ready_to_trade = True

            else:
                ready_to_trade = False

            #Triggers a sell order if a rule is met:
            if ready_to_trade and (time.time() > (new_order.get_key("done_at") + 900)):

                new_trade = client.place_market_order(product_id=new_order.get_key("product_id"), side='sell',
                                                      size=get_size(new_order.get_key("product_id"), new_order.get_key('filled_size')))

                if "id" in new_trade:
                    writer = open(Data.Path, "w")
                    writer.write(new_trade['id'])
                    writer.close()
                    new_order.get_id()

                    if new_order.set_details():
                        print("order sent " + new_order.get_key('product_id'))
                        print("with: ")
                        print(top_rule)
                        print(bottom_rule_used)
                        print(raising_rule)
                        print(falling_rule)
                        funds.capital = float(new_order.get_key('executed_value'))
                        position.set_position()

                    else:
                        pass

                else:
                    print("order details", new_trade)

            #Not rules were true
            else:
                pass

        # If there is a long position but the ticker is not the same as the order's
        # the program will just ignore it
        else:
            pass

        return 'success', 200

    elif request.method == 'GET':
        return render_template('index.html')

    else:
        abort(400)

