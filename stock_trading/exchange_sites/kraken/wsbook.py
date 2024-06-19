import json
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


    def convert_to_float(self, keyvalue):
        return float(keyvalue[0])


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

        self.api_book = json.loads(self.api_data)
        if type(self.api_data) == list:
            if "as" in self.api_data[1]:
                self.api_update_book["ask", self.api_data[1]["as"]]
                self.api_update_book["bid", self.api_data[1]["bs"]]
            elif "a" in self.api_data[1] or "b" in self.api_data[1]:
                for x in self.api_data[1:len(self.api_data[1:]) -1]:
                    if "a" in x:
                        self.api_update_book["ask", x["a"]]
                    if "b" in x:
                        self.api_update_book["bid", x["b"]]
        try:
            yield list(self.api_book['bid'].keys())[0], list(self.api_book['ask'].keys())[0]
        except IndexError:
            yield [], []
