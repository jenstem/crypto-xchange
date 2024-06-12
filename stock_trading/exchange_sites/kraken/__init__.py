import os
import base64
from dotenv import load_dotenv
import hashlib
import hmac
import urllib


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