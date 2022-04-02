from dbconnector import create_TIMELINES
from dbconnector import insert_values
from dbconnector import fetch_timelines
from dbconnector import create_TRADES
from dbconnector import insert_new_trade
from dbconnector import fetch_last_trade
import sqlite3


trade1 = {
    "time": 1648815720,
    "product": "ETHUSD",
    "side": "buy",
    "price": "1350.50",
    "size": "0.91234"
}

trade2 = {
    "time": 1648815780,
    "product": "BTCUSD",
    "side": "sell",
    "price": "45000.50",
    "size": "4.00"
}

trade3 = {
    "time": 1648815840,
    "product": "DOGEUSD",
    "side": "buy",
    "price": ".150",
    "size": "2300.00"
}


def test_timelines():

    connect = sqlite3.connect("../../trading.db")
    connect.execute("DROP TABLE TIMELINES")

    create_TIMELINES(connect)

    insert_values(connect, True, 60, "BTCUSD")
    insert_values(connect, True, 300, "BTCUSD")
    insert_values(connect, False, 900, "BTCUSD")
    insert_values(connect, True, 60, "ETHUSD")
    insert_values(connect, True, 300, "ETHUSD")
    insert_values(connect, True, 900, "ETHUSD")

    fetch_timelines(connect, 'ETHUSD')


def test_trades(a_dict):
    connect = sqlite3.connect("../../trading.db")
    connect.execute("DROP TABLE TRADES")

    create_TRADES(connect)

    insert_new_trade(connect, a_dict)
    fetch_last_trade(connect)


trades = [trade1, trade2, trade3]
for trade in trades:
    test_trades(trade)



