"""Gets the latest dogecoin price and stores it in a DB.

Fetches, prints, and stores the latest dogecoin price form Coinmarketcap.com in a SQL database.

To run:
    python3 doge.py
"""

import json
import psycopg2
import requests
from datetime import datetime







"""
TODO

NEED to get ts to match form twitter and doge.

Fix manually collected data, TS do not match with twitter.

"""









# Manually gathered
prices = [0.002607, 0.002603, 0.00259, 0.002592, 0.00253, 0.002558, 0.002639, 0.002801, 0.002819, 0.002742, 0.002786, 0.002851, 0.002837, 0.002791, 0.002836, 0.002821, 0.002813, 0.003009, 0.002976, 0.002999, 0.00296, 0.003011, 0.003549, 0.00366, 0.003648, 0.004204, 0.004256, 0.003793, 0.003355, 0.00347, 0.00353, 0.00358, 0.003572, 0.003436, 0.0035, 0.003446, 0.003414, 0.003442, 0.0034, 0.003361, 0.003182, 0.003165, 0.00311, 0.003184, 0.003274, 0.003279, 0.00325, 0.003422, 0.004113, 0.00397, 0.004018, 0.004678, 0.005406, 0.004843, 0.004735, 0.004577, 0.004613, 0.00464, 0.004805, 0.004716, 0.004608, 0.004703, 0.004743, 0.005685, 0.0137, 0.01387, 0.01142, 0.01022, 0.01085, 0.01053, 0.01029, 0.01074, 0.01087, 0.009858, 0.009145, 0.008646, 0.01003, 0.009796, 0.009531, 0.009367, 0.009295, 0.009613, 0.009153, 0.009089, 0.008769, 0.008808, 0.008951, 0.008879, 0.008455, 0.008259, 0.03418, 0.07797, 0.0499, 0.04529, 0.04325, 0.03493, 0.03911, 0.05787, 0.05374, 0.05831, 0.08436, 0.08495, 0.08313, 0.08109, 0.0743, 0.07261, 0.07165, 0.06645, 0.06392, 0.05967, 0.05498, 0.0618, 0.0595, 0.06029, 0.05843, 0.06047, 0.05377, 0.05987, 0.05781, 0.05247, 0.05192, 0.05013, 0.05148, 0.05238, 0.05213, 0.05109, 0.05085, 0.0524, 0.05214, 0.06195, 0.06227, 0.05862, 0.0567, 0.05698, 0.06243, 0.06305, 0.05969, 0.05892, 0.05887, 0.05883, 0.05972, 0.06064, 0.05952, 0.05773, 0.05608, 0.05649, 0.05241, 0.05403, 0.05543, 0.05475, 0.05465, 0.05543, 0.05447, 0.07011, 0.06225, 0.05948, 0.05811, 0.06015, 0.06505, 0.0673, 0.06175, 0.06391, 0.06507, 0.07924, 0.07499, 0.09518, 0.1425, 0.1873, 0.4377, 0.3745, 0.3499, 0.4318, 0.4223, 0.347, 0.3088, 0.2684, 0.2894, 0.2888, 0.2805]
ts = [1604041200, 1604127600, 1604214000, 1604304000, 1604390400, 1604476800, 1604563200, 1604649600, 1604736000, 1604822400, 1604908800, 1604995200, 1605081600, 1605168000, 1605254400, 1605340800, 1605427200, 1605513600, 1605600000, 1605686400, 1605772800, 1605859200, 1605945600, 1606032000, 1606118400, 1606204800, 1606291200, 1606377600, 1606464000, 1606550400, 1606636800, 1606723200, 1606809600, 1606896000, 1606982400, 1607068800, 1607155200, 1607241600, 1607328000, 1607414400, 1607500800, 1607587200, 1607673600, 1607760000, 1607846400, 1607932800, 1608019200, 1608105600, 1608192000, 1608278400, 1608364800, 1608451200, 1608537600, 1608624000, 1608710400, 1608796800, 1608883200, 1608969600, 1609056000, 1609142400, 1609228800, 1609315200, 1609401600, 1609488000, 1609574400, 1609660800, 1609747200, 1609833600, 1609920000, 1610006400, 1610092800, 1610179200, 1610265600, 1610352000, 1610438400, 1610524800, 1610611200, 1610697600, 1610784000, 1610870400, 1610956800, 1611043200, 1611129600, 1611216000, 1611302400, 1611388800, 1611475200, 1611561600, 1611648000, 1611734400, 1611820800, 1611907200, 1611993600, 1612080000, 1612166400, 1612252800, 1612339200, 1612425600, 1612512000, 1612598400, 1612684800, 1612771200, 1612857600, 1612944000, 1613030400, 1613116800, 1613203200, 1613289600, 1613376000, 1613462400, 1613548800, 1613635200, 1613721600, 1613808000, 1613894400, 1613980800, 1614067200, 1614153600, 1614240000, 1614326400, 1614412800, 1614499200, 1614585600, 1614672000, 1614758400, 1614844800, 1614931200, 1615017600, 1615104000, 1615190400, 1615276800, 1615363200, 1615449600, 1615536000, 1615622400, 1615708800, 1615791600, 1615878000, 1615964400, 1616050800, 1616137200, 1616223600, 1616310000, 1616396400, 1616482800, 1616569200, 1616655600, 1616742000, 1616828400, 1616914800, 1617001200, 1617087600, 1617174000, 1617260400, 1617346800, 1617433200, 1617519600, 1617606000, 1617692400, 1617778800, 1617865200, 1617951600, 1618038000, 1618124400, 1618210800, 1618297200, 1618383600, 1618470000, 1618556400, 1618642800, 1618729200, 1618815600, 1618902000, 1618988400, 1619074800, 1619161200, 1619247600, 1619334000, 1619420400]

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
            conn = psycopg2.connect("dbname=powerornahh user=powerornahh")
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
            conn = psycopg2.connect("dbname=powerornahh user=powerornahh")
            # create a new cursor
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
        today_ts = int(datetime(today.year, today.month, today.day).timestamp())
        self._insert_items([[today_ts, price]])
        print(f"Latest doge price: ${price}")


if __name__ == "__main__":
    Doge().run()