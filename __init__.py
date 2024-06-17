import os
from dotenv import load_dotenv
import json
from stock_trading.exchange_sites.kraken import *

load_dotenv()

client = os.environ.get("KRAKEN_API_KEY")

def get_trading_pairs() -> list:
    exchange_info = client.get_exchange_info()
    trading_pairs = []
    for s in exchange_info['symbols']:
        trading_pairs.append(s['symbol'])

    return trading_pairs

prices = client.get_all_tickers()

address = client.get_deposit_address(coin='BTC')

def stock_watcher(ws, data):
    print("----------")
    print(json.loads(data))
    print("----------")