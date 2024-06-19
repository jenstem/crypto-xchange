import sys
from stock_trading import trading_opportunity


print(sys.argv)
if len(sys.argv) < 3:
    print("Usage: %s symbol depth" % sys.argv[0])
    print("Example: %s xbt/usd 10" % sys.argv[0])
    sys.exit(1)

while True:
    trading_opportunity("usdt", "bnb", "btc")

    exit()
