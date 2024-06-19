from models import Database
from stock_trading.exchange_sites.kraken.wsbook import WSBookKraken


class CryptoXchanges(WSBookKraken):
    def __init__(self, args):
        WSBookKraken.__init__(self, args)
        self.database = Database()