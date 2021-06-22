from flask import request
from open_position import OpenPosition
from open_authenticated import Order
from get_indicators import GetAnyMACD
from cbpro.authenticated_client import AuthenticatedClient
from webhookListener import get_time
import Data

key = Data.API_Public_Key
b64secret = Data.API_Secret_Key
passphrase = Data.Passphrase


client = AuthenticatedClient(key, b64secret, passphrase)
new_order = Order()
x = OpenPosition(order=new_order)

new_request = request.get_json()

if (new_request['hist'] > 0) and (x.get_position() == False):

    macd_15m_period = GetAnyMACD()
    macd_15m_period.set_candles(product="ETH-USD", callback=get_time(27945), new_gra=300)
    macd_15m_period.set_any_MACD()

    if macd_15m_period.get_hist() > 0:

        macd_5m_period = GetAnyMACD
        macd_5m_period.set_candles(product="ETH-USD", callback=get_time(83835), new_gra=900)
        macd_5m_period.set_any_MACD()

        if macd_5m_period.get_hist() > 0:
            track_trade = client.place_market_order(product_id="ETH-USD", side="buy", funds="5.00")
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

elif (new_request['hist'] < 0) and (x.get_position() == True):

    track_trade = client.place_market_order(product_id=new_order.product, side="sell", funds=new_order.funds)
    new_order.id = track_trade.get("id")
    track_order = client.get_order(str(new_order.id))
    new_order.status = track_order.get("done_reason")

    if new_order.status == 'filled':
        x.open_position = False
