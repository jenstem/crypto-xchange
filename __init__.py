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


def trading_paths(pairs_trio, pairs_info):
    print(pairs_trio)
    trading_value = float(pairs_info[pairs_trio[1][1][0]])
    base_price = (1 / float(pairs_info[pairs_trio[0][1][0]]))
    _rate = 1 + float(pairs_info[pairs_trio[0][3]]) + float(pairs_info[pairs_trio[1][3]]) + float(pairs_info[pairs_trio[2][2]])
    cross_rate = base_price * trading_value * float(pairs_info[pairs_trio[2][0][0]])
    if _rate > cross_rate:
        cross_rate = (1 / float(pairs_info[pairs_trio[2]][1][0])) * float(pairs_info[pairs_trio[1]][0][0])* float(pairs_info[pairs_trio[0]][0][0])

    profit = base_price - cross_rate

    return str(cross_rate), _rate, profit