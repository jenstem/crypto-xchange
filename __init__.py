import os
from dotenv import load_dotenv
import json
import pickle
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


def market_close():
    print("Market is closed")


def build_trading_pairs(*args) -> list:
    pairs = []
    stored_pairs_path = "".join(args)
    if os.path.exists(stored_pairs_path):
        with open(stored_pairs_path, 'rb') as f:
            pairs = pickle.load(f.read())
    else:
        for p in args:
            i = 0
            while args.__len__() > i:
                pair = p + args[i]
                if pair.upper() in get_trading_pairs():
                    pairs.append(pair.upper())
                i += 1
            with open(stored_pairs_path, 'wb') as f:
                f.write(pickle.dumps(pairs))

    return pairs