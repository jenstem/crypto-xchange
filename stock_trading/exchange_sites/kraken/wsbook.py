import json
import sys
from stock_trading.exchange_sites.kraken import kraken
from websocket import create_connection


class WSBookKraken:
    """
    A class to manage the WebSocker connection to the Kraken exchange's order book.

    Attributes:
        ws:  WebSocket connection object.
        api_feed: Type of data feed (default is "Book").
        api_symbol: Trading pair symbol.
        api_depth: Depth of te order book to retrieve.
        api_domain: WebSocket domain for public or private access.
        api_book: Dictionary to hold bid and ask data.
        api_data: Subscription data for the WebSocket.
    """
    def __init__(self, cmd, scope="public"):
        """
        Initializes the WebSocket connection and subscription data.

        Parameters:
            cmd (list): Command containing the trading pair and depth.
            scope (str): Access level for the WebSocket ('public' or 'private').
        """
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


    def callback_function(self):
        """
        Callback function to sort the order book.
        """
        self.sort_book()

    def convert_to_float(self, keyvalue):
        """
        Converts the first element of a key-value pair to float.

        Parameters:
            keyvalue (tuple): A tuple containing price and volume.

        Returns:
            float: The price as a float.
        """
        return float(keyvalue[0])

    def sort_book(self):
        """
        Sorts and prints the current state of the order book.
        """
        bid = sorted(self.api_book['bid'].items(), key=self.convert_to_float, reverse=True)
        ask = sorted(self.api_book['ask'].items(), key=self.convert_to_float)
        print("Bid__________Ask")
        for x in range(int(self.api_depth)):
            print("%(bidprice)s %(bidvolume)s____%(askprice)s (%(askvolume)s)" %
                    {"bidprice": bid[x][0], "bidvolume": bid[x][1], "askprice": ask[x][0], "askvolume": ask[x][1]})

    def api_update_book(self, side, data):
        """
        Updates the order book with new bid or ask data.

        Parameters:
            side (str): 'bid' or 'ask' to specify which side to update.
            data (list): List of price and volume pairs.
        """
        for x in data:
            price_level = x[0]
            if float(x[1]) != 0.0:
                self.api_book[side].update({price_level: float(x[1])})
            else:
                if price_level in self.api_book[side]:
                    self.api_book[side].pop[price_level]
        if side == "bid":
            self.api_book["bid"] = dict(
                sorted(self.api_book["bid"].items(), key=self.convert_to_float, reverse=True)[:int(self.api_depth)])
        elif side == "ask":
            self.api_book["ask"] = dict(
                sorted(self.api_book["ask"].items(), key=self.convert_to_float)[:int(self.api_depth)])

    def ws_connect(self):
        """
        Establishes the WebSocket connection to the Kraken API.
        """
        try:
            self.ws = create_connection(self.api_domain)
        except Exception as e:
            print("Error: WebSocket failed to connect" % e)
            sys.exit(1)

    def send(self):
        """
        Sends the subscription request to the WebSocket.
        """
        try:
            self.ws.send(self.api_data)
        except Exception as e:
            print("Error: Feed subscription failed (%s)" % e)
            self.ws.close()
            sys.exit(1)

    def receive(self):
        """
        Receives messages from the WebSocket and updates the order book.
        """
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
