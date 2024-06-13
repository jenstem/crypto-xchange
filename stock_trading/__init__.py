import os
import json


def stock_watcher(data):
    print("------------")
    print(json.loads(data))
    print("------------")


# Notification for closing
def market_closed():
    print("------------")
    print("Stock market is closed")
    print("------------")
