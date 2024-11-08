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


def on_close():
        print("---Closed---")


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


def calculate_trading_opportunity(pairs_info):
    cross_rate = float
    trade_order = [0, 0, 0]
    for key, value in pairs_info.items():
        cross_rate = (1 / float(pairs_info[key[1][0]]))
        if trade_order[0] == 0:
            trade_order[0] = key
            continue
        if key.startswith(trade_order[0][:2]):
            trade_order[1] = key
        else:
            trade_order[2] = key

    print(trading_paths(trade_order, pairs_info, value))


def trade_ordering(stock_pairs):
    trade_order = {}
    for pair in stock_pairs:
        for p in stock_pairs:
            if p == pair:
                trade_order[p] = "buy"
            else:
                trade_order[p] = "sell"

    return trade_order


def trading_opportunity(*args):
    try:
        t_pairs = build_trading_pairs(*list(*args))
        t_pairs_info = {}
        for pair in t_pairs:
            get_order = client.get_order_book(symbol=pair)
            trade_fee = client.get_trade_fee(symbol=pair)
            marker = trade_fee[0]['makerCommission']
            taker = trade_fee[0]['takerCommission']
            t_pairs_info[pair] = [get_order['bids'][0], get_order['asks'][0], marker, taker]

        calculate_trading_opportunity(t_pairs_info)
    except Exception as e:
        print(e)