from dbconnector import Timelines
from dbconnector import Trades
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

    timeline = Timelines()

    timeline.create_table()

    timeline.insert_values(True, 60, "BTCUSD")
    timeline.insert_values(True, 300, "BTCUSD")
    timeline.insert_values(False, 900, "BTCUSD")
    timeline.insert_values(True, 60, "ETHUSD")
    timeline.insert_values(True, 300, "ETHUSD")
    timeline.insert_values(True, 900, "ETHUSD")

    cursor = timeline.fetch_row('ETHUSD')
    for line in cursor:
        print(line)


def test_trades(vals):

    trades = Trades()

    trades.create_table()

    for v in vals:
        trades.insert_values(v)
        cursor = trades.fetch_row()

        for line in cursor:
            print(line)


timelines = Timelines()
cursor = timelines.fetch_all()
for c in cursor:
    print(c)
