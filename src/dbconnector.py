import sqlite3
import Data

connect = sqlite3.connect("../../trading.db")


def create_TIMELINES(connection):
    connection.execute(''' CREATE TABLE IF NOT EXISTS TIMELINES (
                PRODUCT TEXT PRIMARY KEY NOT NULL,
                TIMELINE_1M NUMERIC, 
                TIMELINE_5M NUMERIC, 
                TIMELINE_15M NUMERIC
                );
                ''')
    connection.commit()


def insert_values(connection, value, timeline, product):

    column = None
    if timeline == 60:
        column = "TIMELINE_1M"
    elif timeline == 300:
        column = "TIMELINE_5M"
    elif timeline == 900:
        column = "TIMELINE_15M"

    connection.execute(f"INSERT INTO TIMELINES ({column}) VALUES ({value}) WHERE PRODUCT = '{product}';")

    connection.commit()


def fetch_timelines(connection, product):
    cursor = connection.execute(f"SELECT * FROM TIMELINES WHERE PRODUCT = '{product}';")
    for row in cursor:
        print(row)


def create_TRADES(connection):
    connection.execute('''CREATE TABLE IF NOT EXISTS TRADES (
                        TIME REAL PRIMARY KEY NOT NULL, 
                        PRODUCT TEXT NOT NULL, 
                        SIDE TEXT NOT NULL,
                        PRICE REAL NOT NULL, 
                        SIZE REAL NOT NULL,
                        )
                        ''')
    connection.commit()


def insert_new_trade(connection, values):
    connection.execute(f"INSERT OR REPLACE INTO TRADES \
                       VALUES({values['time']}, \
                              {values['product']}, \
                              {values['side']}, \
                              {values['price']}, \
                              {values['size']}) ")
    connection.commit()


def fetch_last_trade(connection):
    cursor = connection.execute(f"SELECT * FROM TRADES \
                       ORDER BY TIME DESC \
                       LIMIT 1")
    return cursor
