from flask import request
from open_position import OpenPosition
from order import Order
from capital import Capital
from cbpro.authenticated_client import AuthenticatedClient
from eth_data import webhooks
from app_methods import *
from indicators import *
import Data

key = Data.API_Public_Key
b64secret = Data.API_Secret_Key
passphrase = Data.Passphrase


client = AuthenticatedClient(key, b64secret, passphrase)
new_order = Order(client)
position = OpenPosition(new_order)
funds = Capital(client)

for request in webhooks:

    new_request = request

    # If there is no a position opened it will trigger a buy order
    if position.get_position() is False:

        new_ticker = new_request['ticker']
        if float(new_request['hist']) > 0 and float(new_request['volume']) > float(new_request['volumema']):

            indicator = Indicator(client)
            indicator.set_candles(product=get_key('ticker', new_request), callback=get_time(27976), begin=get_time(0),
                                  granularity=300)
            indicator.get_data_set()
            indicator.reverse_data()
            indicator.get_np_array()
            macd_5m = MACD(client=client)
            macd_5m.np_array = indicator.np_array
            macd_5m.get_MACD()
            volume_5m = VolSMA(client=client, timeperiod=20)
            volume_5m.candles = indicator.candles
            volume_5m.get_data_set()
            volume_5m.reverse_data()
            volume_5m.get_np_array()
            volume_5m.get_volume()

            # Buy if True
            if macd_5m.hist[-1] > 0 and volume_5m.data_array[-1] > volume_5m.real[-1]:
                new_trade = client.place_market_order(product_id=get_key('ticker', new_request),
                                                      side="buy",
                                                      funds=funds.get_capital())
                print(new_trade)
                if new_order.set_details(new_id=new_trade.get('id')):
                    position.set_position()
                    print("order sent " + new_order.get_key('product_id') + " " + new_order.get_key('funds'))

            # Buy if True
            elif macd_5m.macd[-2] > macd_5m.macd[-3]:
                new_trade = client.place_market_order(product_id=get_key('ticker', new_request),
                                                      side="buy",
                                                      funds=funds.get_capital())
                print(new_trade)
                if new_order.set_details(new_id=new_trade.get('id')):
                    position.set_position()
                    print("order sent " + new_order.get_key('product_id') + " " + new_order.get_key('funds'))

            else:
                print("requirements were not met for ", get_key('ticker', new_request))
            # Does nothing if both statements are False

    # If the Post request ticker is the same as the order's it will trigger a sell order
    elif position.get_position() and get_key('ticker', new_request) == new_order.get_key('product_id'):

        # Sell if True
        if new_request['hist'] < 0 and float(new_request['volume']) > float(new_request['volumema']):
            new_trade = client.place_market_order(product_id=new_order.get_key("product_id"),
                                                  side='sell',
                                                  size=new_order.get_key('filled_size'))
            print(new_trade)
            if new_order.set_details(new_id=new_trade.get('id')):
                print("order sent " + new_order.get_key('product_id') + " " + new_order.get_key('funds'))
                funds.capital = float(new_order.get_key('executed_value'))
                position.set_position()
            print("order sent " + new_order.get_key('product_id') + " " + new_order.get_key('funds'))

    elif position.get_position() and get_key('ticker', new_request) != new_order.get_key('product_id'):

        print("ticker does not match the product id from order")

    # If there is a long position but the ticker is not the same as the order's
    # the program will just ignore it
    else:
        print("Nothing to do")
        pass


