import os
from arbitrage_trading.utils import create_xlsx
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
            cursor.execute("SELECT * FROM assets")

            investment = []
            data = []

            assets = cursor.fetchall()

            for row in assets:
                cursor.execute(f"SELECT * FROM price WHERE symbol = '{row[1]}'")
                container = cursor.fetchall()
                if container.__len__() >= 2:
                    profit = round(float(container[1][2] - float(container[0][2])), 2)
                    profit_gain = round(float(profit / float(container[0][2]) * 100), 2)
                    if profit_gain > 1:
                        investment.append([row[1], profit, profit_gain])
                        data += ([row[1], profit, profit_gain])

            headers = ['Stock Symbol', 'Profit', 'Profit Gain']
            create_xlsx('Potential Investment', headers, investment)

            self.db.close()
        except Exception as e:
            print(e)