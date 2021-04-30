"""Gets the latest dogecoin price and stores it in a DB.

Fetches, prints, and stores the latest dogecoin price form Coinmarketcap.com in a SQL database.

To run:
    python3 doge.py
"""

import json
import os
import psycopg2
import pytz
import re
import requests
from datetime import datetime


_NAME = None
__NAME = None
_PASS = None
_HOST = '127.0.0.1'
_PORT = '5432'
_tz = pytz.timezone("America/Los_Angeles")

# Parses db url if running on heroku
if(os.environ['PWD'].find("app") >= 0):
    db_url_pattern = """
        postgres://(?P<_NAME>\w*):(?P<pass>\w*)@(?P<host>[\w\-\.]*):(?P<port>\d*)\/(?P<name>\w*)
    """
    m = re.search(re.compile(db_url_pattern, re.MULTILINE | re.VERBOSE),
                os.environ['DATABASE_URL'])

    _NAME = m.group('name')
    __NAME = m.group('name')
    _PASS = m.group('pass')
    _HOST = m.group('host')
    _PORT = m.group('port')
else:
    _NAME = os.environ['NAME']
    __NAME = os.environ['NAME']
    _PASS = os.environ['PASS']


class Doge:
    def _create_table(self):
        """ Creates a table to store doge coin prices. """
        sql = """CREATE TABLE IF NOT EXISTS doge(
            id SERIAL PRIMARY KEY,
            ts NUMERIC NOT NULL,
            price NUMERIC not NULL,
            UNIQUE (ts, price)
            )"""
        conn = None
        try:
            conn = psycopg2.connect(f"dbname={_NAME} user={_NAME} host={_HOST} password={_PASS} port={_PORT}")
            # create a new cursor
            cur = conn.cursor()
            cur.execute(sql)
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Psql error: {error}")
        finally:
            if conn is not None:
                conn.close()

    def _insert_items(self, items):
        """ Insert multiple values into a table."""
        sql = "INSERT INTO doge(ts, price) VALUES(%s, %s) ON CONFLICT DO NOTHING;"
        conn = None
        try:
            conn = psycopg2.connect(f"dbname={_NAME} user={_NAME} host={_HOST} password={_PASS} port={_PORT}")
            cur = conn.cursor()
            # execute the INSERT statement
            cur.executemany(sql,items)
            # commit the changes to the database
            conn.commit()
            # close communication with the database
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Psql error: {error}")
        finally:
            if conn is not None:
                conn.close()

    def _get_latest_doge_price(self):
        """ Gets the latest doge coin price in USD.

        Returns:
            price: The price of dogecoin in USD as reported by Coinmarketcap.com.
        """
        url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
        params = {
            "symbol": "DOGE",
            "convert": "USD"
        }

        headers = {
            "X-CMC_PRO_API_KEY": "52822ab1-967a-42eb-8481-e9a06ce4d559",
            "Accept": "application/json"
        }
        res  = requests.get(url, headers=headers, params=params)
        return json.loads(res.text)['data']['DOGE']['quote']['USD']['price']

    def run(self):
        """Finds and stores the latest dogecoin price."""
        self._create_table()
        price = self._get_latest_doge_price()
        today = datetime.now().date()
        today_ts = int(
            _tz.localize(
                datetime(today.year, today.month, today.day)).timestamp())
        self._insert_items([[today_ts, price]])
        print(f"Latest doge price: ${price}")


if __name__ == "__main__":
    Doge().run()