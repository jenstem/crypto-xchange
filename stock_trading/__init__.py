import json
from models import Database
from stock_trading.exchange_sites.kraken.wsbook import WSBookKraken


class CryptoXchanges(WSBookKraken):
    def __init__(self, args):
        WSBookKraken.__init__(self, args)
        self.database = Database()

    def exchange_watcher(self, data):
        try:
            prices = json.loads(data)
            k_prices = list(self.get_data())[0]
            print("Kraken", k_prices)
            t_text = "Buy {:.5f} on Kraken".format(float(k_prices[0]))
            print(t_text)

        except Exception as e:
            print(str(e))

    def on_close(self):
        print("---Closed---")