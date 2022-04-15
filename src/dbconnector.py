import sqlite3
import Data


class Database:

    def __init__(self):
        self.connect = sqlite3.connect("../../trading.db")

    def create_table(self):
        pass

    def fetch_all(self):
        pass


class Timelines(Database):

    def __init__(self):
        super(Timelines, self).__init__()

    def create_table(self):
        #self.connect.execute("DROP TABLE TIMELINES")
        self.connect.execute(''' CREATE TABLE IF NOT EXISTS TIMELINES (
                    PRODUCT TEXT PRIMARY KEY NOT NULL,
                    TIMELINE_1M NUMERIC, 
                    TIMELINE_5M NUMERIC, 
                    TIMELINE_15M NUMERIC
                    );
                    ''')
        self.connect.commit()

    def insert_values(self, value, timeline, product):

        column = None
        if timeline == 60:
            column = "TIMELINE_1M"
        elif timeline == 300:
            column = "TIMELINE_5M"
        elif timeline == 900:
            column = "TIMELINE_15M"

        try:
            self.connect.execute(f"INSERT INTO TIMELINES (PRODUCT, {column}) VALUES ('{product}', {value});")
        except sqlite3.IntegrityError as sqliteIE:
            if sqliteIE.args[0] == "UNIQUE constraint failed: TIMELINES.PRODUCT":
                self.connect.execute(f"UPDATE TIMELINES SET {column} = {value} WHERE PRODUCT = '{product}';")

        self.connect.commit()
        self.connect.close()

    def fetch_row(self, product):
        cursor = self.connect.execute(f"SELECT * FROM TIMELINES WHERE PRODUCT = '{product}';")
        return cursor

    def fetch_all(self):
        cursor = self.connect.execute(f"SELECT * FROM TIMELINES")
        return cursor


class Trades(Database):

    def __init__(self):
        super(Trades, self).__init__()

    def create_table(self):
        #self.connect.execute("DROP TABLE TRADES")
        self.connect.execute('''CREATE TABLE IF NOT EXISTS TRADES (
                            TIME REAL PRIMARY KEY NOT NULL, 
                            PRODUCT TEXT NOT NULL, 
                            SIDE TEXT NOT NULL,
                            PRICE REAL NOT NULL, 
                            SIZE REAL NOT NULL
                            );
                            ''')
        self.connect.commit()

    def insert_values(self, values):
        self.connect.execute(f"INSERT INTO TRADES VALUES({values['time']}, '{values['product']}', '{values['side']}', \
                           '{values['price']}', '{values['size']}'); ")
        self.connect.commit()

    def fetch_row(self):
        cursor = self.connect.execute(f"SELECT * FROM TRADES ORDER BY TIME DESC LIMIT 1")
        return cursor

    def fetch_all(self):
        cursor = self.connect.execute(f"SELECT * FROM TRADES ORDER BY TIME DESC")
        return cursor
