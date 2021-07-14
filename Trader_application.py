from flask import request
from open_position import OpenPosition
from order import Order
from capital import Capital
from cbpro.authenticated_client import AuthenticatedClient
from app_methods import *
from indicators import *
import Data

key = Data.API_Public_Key
b64secret = Data.API_Secret_Key
passphrase = Data.Passphrase


client = AuthenticatedClient(key, b64secret, passphrase)
new_order = Order()
position = OpenPosition(new_order)
funds = Capital(client)

if request.method == 'POST':

    new_request = request.get_json(force=True)

    # If there is no a position opened it will trigger a buy order
    if position.get_position() is False:

        new_ticker = new_request['ticker']
        if float(new_request['hist']) > 0 and float(new_request['volume']) > float(new_request['volumema']):

            indicator = Indicator(client)
            indicator.set_candles(product=new_ticker, callback=get_time(27976), begin=get_time(0), granularity=300)
            indicator.get_data_set()
            indicator.reverse_data()
            indicator.get_np_array()
            macd_5m = MACD()
            macd_5m.np_array = indicator.np_array
            macd_5m.get_MACD()
            volume_5m = VolSMA()
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
                new_order.set_details(new_trade.get('id'))
                position.set_position()
                print("order sent " + new_order.get_key('product_id') + " " + new_order.get_key('funds'))

            # Buy if True
            elif macd_5m.macd[-2] > macd_5m.macd[-3]:
                new_trade = client.place_market_order(product_id=get_key('ticker', new_request),
                                                      side="buy",
                                                      funds=funds.get_capital())
                new_order.set_details(new_trade.get('id'))
                position.set_position()
                print("order sent " + new_order.get_key('product_id') + " " + new_order.get_key('funds'))

            # Does nothing if both statements are False

    # If the Post request ticker is the same as the order's it will trigger a sell order
    elif position.get_position() and new_request['ticker'] == new_order.get_key('product_id'):

        # Sell if True
        if new_request['hist'] < 0 and float(new_request['volume']) > float(new_request['volumema']):
            new_trade = client.place_market_order(product_id=new_order.get_key("product_id"),
                                                  side='sell',
                                                  size=new_order.get_key('filled_size'))

            new_order.set_details(new_trade.get("id"))
            funds.capital = float(new_order.get_key('executed_value'))
            print("order sent " + new_order.get_key('product_id') + " " + new_order.get_key('funds'))
            position.set_position()

    # If there is a long position but the ticker is not the same as the order's
    # the program will just ignore it
    else:
        pass


