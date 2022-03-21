import sqlite3

connect = sqlite3.connect("../../trading.db")

connect.execute(''' CREATE TABLE timeline_ready (
                PRODUCT TEXT,
                TIMELINE_1M REAL, 
                TIMELINE_5M REAL, 
                TIMELINE_15M REAL
                )
                ''')
