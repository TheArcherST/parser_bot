from .types import UpdateFrame, DataPrice, DataShorts
import sqlite3 as sql
import pandas as pd
from datetime import datetime


class SPCEOptionsChainDB:
    path = 'data/spce.db'

    def __init__(self):
         with sql.connect(self.path) as conn:
             cursor = conn.cursor()
             cursor.execute("""CREATE TABLE IF NOT EXISTS spce_options_chain_history (
                expires DATE,
                strike_price REAL,
                put_or_call TEXT,
                volume REAL
             )""")
             conn.commit()
             cursor.close()

    def write_updates(self, updates: pd.DataFrame):
        with sql.connect(self.path) as conn:
            cursor = conn.cursor()
            for index, series in updates.iterrows():
                cursor.execute("""INSERT INTO spce_options_chain_history VALUES (?, ?, ?, ?)
                """, (series[0], series[1], series[2], series[3]))
            conn.commit()
            cursor.close()

    def get_df(self, length):
        with sql.connect(self.path) as conn:
            df = pd.read_sql(f"SELECT * FROM spce_options_chain_history LIMIT {length}", conn)

        return df


class SPCEDB:
    path = 'data/spce.db'

    def __init__(self):
         with sql.connect(self.path) as conn:
             cursor = conn.cursor()
             cursor.execute("""CREATE TABLE IF NOT EXISTS spce_history (
                write_time DATETIME,
                cost REAL,
                volume REAL,
                average_volume REAL,
                current_short_volume REAL,
                previous_short_volume REAL
             )""")
             conn.commit()
             cursor.close()

    def write_updates(self, updates: UpdateFrame):
        with sql.connect(self.path) as conn:
            cursor = conn.cursor()
            cursor.execute("""INSERT INTO spce_history VALUES (?, ?, ?, ?, ?, ?)
            """, (datetime.now(), updates.data_price.cost, updates.data_price.volume,
                   updates.data_price.average_volume, updates.data_shorts.current_short_volume,
                   updates.data_shorts.previous_short_volume))
            conn.commit()
            cursor.close()

    def get_df(self, length):
        with sql.connect(self.path) as conn:
            df = pd.read_sql(f"SELECT * FROM spce_history LIMIT {length}", conn)

        return df
