import os
import base64
from dotenv import load_dotenv
import hashlib
import hmac
import json
import requests
import time
import urllib
from urllib import request


load_dotenv()


assetAttributeNames = {
    'BTC': 'Bitcoin',
    'ETH': 'Ethereum',
    'LTC': 'Litecoin',
    'USDT': 'Tether',
}


# Generate a signature for the API requests
def get_signature(urlpath, data):
    postdata = urllib.parse.urlencode(data)
    encoded_message = (str(data['nonce']) + postdata).encode()
    message = urlpath.encode() + hashlib.sha256(encoded_message).digest()

    signature = hmac.new(base64.b64decode(os.environ.get("KRAKEN_API_PRIVATE")), message, hashlib.sha512)
    sigdigest = base64.b64encode(signature.digest())
    return sigdigest.decode()


# Generate a nonce for the API requests
def get_token():
    api_nonce = str(int(time.time() * 1000))
    api_post = 'nonce=' + api_nonce

    # Hash algorithms
    api_sha256 = hashlib.sha256(api_nonce.encode('utf-8') + api_post.encode('utf-8'))
    api_hmac = hmac.new(base64.b64decode(os.environ.get("KRAKEN_API_PRIVATE")),
        os.environ.get("KRAKEN_API_PATH").encode('utf-8') + api_sha256.digest(), hashlib.sha512)

    # Signature encoded in base64 for API-Sign value
    api_sign = base64.b64encode(api_hmac.digest())

    # HTTP POST request
    api_request = request.Request('https://api.kraken.com/0/private/GetWebSocketsToken', api_post.encode('utf-8'))
    api_request.add_header('API-Key', os.environ.get("KRAKEN_API_KEY"))
    api_request.add_header('API-Sign', api_sign)
    api_response = request.urlopen(api_request).read().decode()

    print(os.environ.get("KRAKEN_API_KEY"), os.environ.get("KRAKEN_API_PRIVATE"))
    print(json.loads(api_response))

    token = json.loads(api_response)['result']['token']
    print(token)

    return token


    # Attach headers and return the POST request
def api_request(uripath, data):
    headers = {
        'API-Key': os.environ.get("KRAKEN_API_KEY"),
        'API-Sign': get_signature(uripath, data)
    }

    req = requests.post((os.environ.get("KRAKEN_API_URL") + uripath), headers=headers, data=data)
    return req


# Organize the request and print results
def add_order(order):
    results = api_request('/0/private/AddOrder'), {
        'nonce': str(int(time.time() * 1000)),
        'pair': "XBTUSD",
        'type': "buy",
        'ordertype': "market",
        'price': 27500,
        'volume': 1.25,
    }

    print(results.json())
