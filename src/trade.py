from dbconnector import create_TIMELINES
from dbconnector import insert_values
from dbconnector import fetch_timelines
from dbconnector import create_TRADES
from dbconnector import insert_new_trade
from dbconnector import fetch_last_trade
import sqlite3

connect = sqlite3.connect("../../trading.db")
connect.execute("DROP TABLE TIMELINES")

create_TIMELINES(connect)

insert_values(connect, True, 60, "BTCUSD")

fetch_timelines(connect, 'BTCUSD')
