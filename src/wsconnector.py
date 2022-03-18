import json
import time
from dict import new_dict
from datetime import datetime
from candleStick import CandleStick
from indicators import MACD
from threading import Thread
from websocket import create_connection, WebSocketConnectionClosedException


n_dict = {
    "ETH-USD": 1
}


#Populates a dict with classes using the keys from the products dict
def populate_dict(a_dict):
    cl_dict = {}
    for key in a_dict:
        cl_dict[key] = [CandleStick(key, 60), CandleStick(key, 300), CandleStick(key, 900)]
    return cl_dict


#access a candlesticks dict and gets the list representing the candlesticks for the product
def get_candlesticks(a_dict, product, timeline: int):
    try:
        a_candle = a_dict[product][timeline]
        return a_candle
    except ValueError as ve:
        return f"Tried to get candlesticks for {product}."


def populate_list(a_dict):
    products = []
    for key in a_dict:
        products.append(key)
    return products


def main():

    candlesticks = populate_dict(new_dict)
    product_ids = populate_list(new_dict)
    ws = create_connection("wss://ws-feed.pro.coinbase.com")
    ws.send(
        json.dumps(
            {
                "type": "subscribe",
                "product_ids": product_ids,
                "channels": ["matches"]
            }
        )
    )

    while ws.connected:
        obj = json.loads(ws.recv())
        candle = None
        if "product_id" in obj:
            i = 0
            for i in range(3):
                candle = get_candlesticks(candlesticks, obj["product_id"], i)
                candle.candle_input(obj)
                candle.read_indicators()


if __name__ == "__main__":
    main()






