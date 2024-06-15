import sys
from stock_trading.exchange_sites.kraken import kraken
from websocket import create_connection


class WSBookKraken:
    def __init__(self, cmd, scope="public"):
        self.ws = None
        self.api_feed = "Book"
        self.api_symbol = cmd[1].upper()
        self.api_depth = cmd[2]
        self.api_domain = "wss://ws.kraken.com/"
        if scope == "private":
            self.api_domain = "wss://ws-auth.kraken.com/"

        self.api_book = {"bid": {}, "ask": {}}
        self.api_data = '{"event":"subscribe", "subscription":{"name":"%(feed)s", "depth":%(depth)s,' \
                        '"token":"%(token)s"}, "pair":["%(symbol)s"]}' \
                        % {"feed": self.api_feed, "depth": self.api_depth, "symbol": self.api_symbol,
                        "token": kraken.get_token()}

        self.ws_connect()
        self.send()


    def ws_connect(self):
        try:
            self.ws = create_connection(self.api_domain)
        except Exception as e:
            print("Error: WebSocket failed to connect" % e)
            sys.exit(1)

    def send(self):
        try:
            self.ws.send(self.api_data)
        except Exception as e:
            print("Error: Feed subscription failed (%s)" % e)
            self.ws.close()
            sys.exit(1)

    def receive(self):
        try:
            self.api_data = self.ws.recv()
        except KeyboardInterrupt:
            self.ws.close()
            sys.exit(0)
        except Exception as e:
            print("Error: WebSocket message failed (%s)" % e)
            self.ws.close()
            sys.exit(1)
