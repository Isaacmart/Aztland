import json
import time
import os
import psutil
from dict import new_dict
from datetime import datetime
from candleStick import CandleStick
from indicators import MACD
from threading import Thread
from threading import Lock
from dbconnector import Timelines
from websocket import create_connection, WebSocketConnectionClosedException


n_dict = {
    "UNFI-USD": 1
}


#Populates a dict with classes using the keys from the products dict
def populate_dict(a_dict: dict):
    cl_dict = {}

    for key in a_dict:
        cl_dict[key] = [CandleStick(key, 60), CandleStick(key, 300), CandleStick(key, 900)]

    return cl_dict


#access a candlesticks dict and gets the candlestick for a product with timeline
def get_candlesticks(a_dict: dict, product, timeline: int):

    #Tries to get a candlestick object for timeline
    try:
        a_candle = a_dict[product][timeline]
        return a_candle
    except ValueError as ve:
        return f"Tried to get candlesticks for {product}."


#Creates a list of products
def populate_list(a_dict):
    products = []

    for key in a_dict:
        products.append(key)

    return products


#Process an incoming json file
def handle_json(job, candlesticks):
    thread = Thread(target=json_thread(job, candlesticks))
    thread.start()
    thread.join()
    print("finished processing json", time.time())


#Body of thread that process a json object
def json_thread(job, candlesticks):

    for i in range(3):
        # returns a Candlestick object for timeline i
        candle = get_candlesticks(candlesticks, job["product_id"], i)
        # Updates candlesticks with the given json object
        candle.candle_input(job)

    pr = job["product_id"].replace('-', '')
    connect = Timelines()
    cursor = connect.fetch_row(pr)
    for line in cursor:
        if line[1] and line[2] and line[3]:
            print(job["product_id"] + + str(time.time()))


def main():

    print(os.getpid())
    candlesticks = populate_dict(n_dict)
    product_ids = populate_list(n_dict)
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
        #Json objects obtained from Coinbase
        obj = json.loads(ws.recv())

        if "product_id" in obj:
            print("started processing websocket", time.time())
            handle_json(obj, candlesticks)


if __name__ == "__main__":
    main()
