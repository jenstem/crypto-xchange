import os
from stock_trading.utils import create_xlsx
from dotenv import load_dotenv
from mysql import connector

load_dotenv()

# Establish connection to DB
class Database:
    def __init__(self):
        self.db = connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            db=os.getenv('DB_NAME')
        )

    def get_assets(self):
        try:
            cursor = self.db.cursor()
            cursor.execute("SELECT DISTINCT stock_symbol FROM price;")

            investment = []
            data = []

            assets = cursor.fetchall()

            for row in assets:
                cursor.execute(f"SELECT * FROM price WHERE stock_symbol = '{row[1]}' ORDER BY ask DESC")
                container = cursor.fetchall()
                if container.__len__() >= 2:
                    profit = round(float(container[0][6] - float(container[-1][5])), 2)
                    profit_gain = round(profit * 100 / float(container[0][6]), 2)
                    if profit_gain > 1:
                        investment.append(f"{profit_gain}% - {container[-1][2]} on {container[-1][1]} at {container[-1][6]} and Sell on {container[0][1]} at {container[0][5]}")
                        data += ([("Buy", container[-1][2], container[-1][1], container[-1][6], f"{profit_gain}%", profit, "Sell", container[0][5], container[0][1])])

            headers = ['Action', 'symbol', 'exchange', 'ask price', 'profit gain', 'expected profit', 'artitrage', 'bid price', 'crypto exchange']
            create_xlsx('Potential Investment', headers, investment)

            self.db.close()
        except Exception as e:
            print(e)