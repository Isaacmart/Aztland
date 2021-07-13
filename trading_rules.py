from flask import request
from open_position import OpenPosition
from order import Order
from get_indicators import GetAnyMACD
from cbpro.authenticated_client import AuthenticatedClient
from eth_data import webhooks
from app_methods import *
import Data

key = Data.API_Public_Key
b64secret = Data.API_Secret_Key
passphrase = Data.Passphrase


client = AuthenticatedClient(key, b64secret, passphrase)
new_order = Order()
x = OpenPosition(order=new_order)

#request_flask =
#{
#  "exchange": "COINBASE",
#  "ticker": "ETHUSD",
#  "price": "2054.43",
#  "volume": "975.23",
#  "hist": "0.23",
#  "macd": "-20.28",
#  "signal": "-20.52"
#}

#request_flask = request.get_json(force=True)
#request_ticker = request_flask['ticker']
#request_currency = get_ticker_product(request_flask["ticker"])

index = 0
for request_flask in webhooks:

    '''print('order number: ', index)
    index += 1
    print("initial capital: ", get_capital('42d739b5-f5cd-48c0-baf6-b905836a1ca4', client=client))'''

    request_currency = get_key('ticker', request_flask)

    if (float(request_flask['hist']) > 0) and (x.get_position() is False):

        macd_15m_period = GetAnyMACD()
        macd_15m_period.set_candles(product=request_currency, callback=get_time(83929),
                                    begin_here=get_time(0), new_gra=900)
        macd_15m_period.set_any_MACD()

        if macd_15m_period.get_hist() > 0:

            macd_5m_period = GetAnyMACD()
            macd_5m_period.set_candles(product=request_currency, callback=get_time(27976),
                                       begin_here=get_time(0), new_gra=300)
            macd_5m_period.set_any_MACD()

            if macd_5m_period.get_hist() > 0:
                track_trade = client.place_market_order(product_id=request_currency, side="buy",
                                                        funds=12.0)
                new_order.id = track_trade.get("id")
                track_order = client.get_order(str(new_order.id))
                new_order.status = track_order.get("done_reason")
                '''print(get_capital('42d739b5-f5cd-48c0-baf6-b905836a1ca4', client=client))
                print(track_trade)
                print(new_order.id)
                print(track_order)
                print(new_order.status)'''

                if new_order.status is not None:

                    new_order.side = track_order.get("side")
                    new_order.product = track_order.get("product_id")
                    new_order.done_at = track_order.get("done_at")
                    new_order.executed_value = track_order.get("executed_value")
                    new_order.size = track_order.get("filled_size")

                    x.set_position()
                    print("New buy order was filled")
                else:
                    print("New buy order was not filled")

            else:
                print("5 minutes period MACD is less than 0")
        else:
            print("15 minutes period MACD is less than 0")

    elif request_currency == new_order.product:

        if float(request_flask['hist']) < 0 and x.get_position():

            track_trade = client.place_market_order(product_id=new_order.product, side="sell", size=new_order.size)
            new_order.id = track_trade.get("id")
            track_order = client.get_order(str(new_order.id))
            new_order.status = track_order.get("done_reason")
            '''print(track_order)
                    print(new_order.id)
                    print(track_order)
                    print(new_order.status)
            '''
            if new_order.status == 'filled':
                x.open_position = False

            print(x.open_position)

            print("Sell order was filled")

    elif (float(request_flask['hist']) > 0) and (x.get_position()):
        print("There is a open position")

    elif (float(request_flask['hist']) < 0) and (x.get_position() is False):
        print("Condition: Histogram must be greater than zero was not met")
