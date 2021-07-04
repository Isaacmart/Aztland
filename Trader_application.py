#create methods to pack trading rules 6/27
#original in trading_rules.py

from flask import request
from open_position import OpenPosition
from open_authenticated import Order
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

new_request = {"exchange": "COINBASE", "ticker": "ETHUSD", "price": "2054.43", "volume": "975.23", "hist": "0.23", "macd": "-20.28", "signal": "-20.52"}

#request_flask = request.get_json(force=True)
#request_ticker = request_flask['ticker']
request_currency = get_ticker_product(new_request["ticker"])


for new_request in webhooks:
    if (float(new_request['hist']) > 0) and (x.get_position() is False):

        macd_15m_period = GetAnyMACD()
        macd_15m_period.set_candles(product=request_currency, callback=get_time(83835), new_gra=900)
        macd_15m_period.set_any_MACD()

        if macd_15m_period.get_hist() > 0:

            macd_5m_period = GetAnyMACD()
            macd_5m_period.set_candles(product=request_currency, callback=get_time(27945), new_gra=300)
            macd_5m_period.set_any_MACD()

            if macd_5m_period.get_hist() > 0:
                track_trade = client.place_market_order(product_id=request_currency, side="buy", funds="5.00")
                new_order.id = track_trade.get("id")
                track_order = client.get_order(str(new_order.id))
                new_order.status = track_order.get("done_reason")

                if new_order.status is not None:
                    new_order.side = track_order.get("side")
                    new_order.product = track_order.get("product_id")
                    new_order.fill_time = track_order.get("done_at")
                    new_order.executed_value = track_order.get("executed_value")
                    new_order.size = order_size = track_order.get("filled_size")

                    x.set_position()
                    print("New buy order was filled")
                else:
                    print("New buy order cannot be filled")

            else:
                print("5 minutes period MACD is less than 0")
        else:
            print("15 minutes period MACD is less than 0")

    elif (float(new_request['hist']) < 0) and (x.get_position() and (request_currency == new_order.product)):

        track_trade = client.place_market_order(product_id=new_order.product, side="sell", funds=new_order.funds)
        new_order.id = track_trade.get("id")
        track_order = client.get_order(str(new_order.id))
        new_order.status = track_order.get("done_reason")

        if new_order.status == 'filled':
            x.open_position = False

        print("Sell order was filled")

    elif (float(new_request['hist']) > 0) and (x.get_position()):
        print("There is a open position")

    elif (float(new_request['hist']) < 0) and (x.get_position() is False):
        print("Condition: Histogram must be greater than zero was not met")


'''
Expected behavior if 15m MACD histogram is below zero:
15 minutes period MACD is less than 0
Condition: Histogram must be greater than zero was not met
15 minutes period MACD is less than 0
Condition: Histogram must be greater than zero was not met
Condition: Histogram must be greater than zero was not met
Condition: Histogram must be greater than zero was not met
15 minutes period MACD is less than 0
15 minutes period MACD is less than 0
Condition: Histogram must be greater than zero was not met
Condition: Histogram must be greater than zero was not met

expected behavior if 15m and 5m MACD histogram is over the zero line:
New buy order was filled
Sell order was filled
New buy order was filled 
Sell order was filled 
Condition: Histogram must be greater than zero was not met
Condition: Histogram must be greater than zero was not met
New buy order was filled
There is a open position
Sell order was filled
Condition: Histogram must be greater than zero was not met
'''

