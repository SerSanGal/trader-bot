
import sys
import os

PACKAGE_PARENT = '../..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

print(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from binance import binance_api, binance_config

import csv
import numpy

b_client = binance_api.BinanceAPI(
    binance_config.api_key, binance_config.api_secret
)


try:
    symbol = sys.argv[1]
except IndexError:
    sys.exit("ERROR: Symbol argument missing")


candles = b_client.get_klines_by_limit(symbol, "1m", 120)

if "msg" in candles:
    sys.exit("ERROR: " + candles["msg"] )

data = [["close_time", "close"]]
for candle in candles:
    data.append([candle[6], numpy.double(candle[4])])

with open("tests/data/"+symbol+".csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(data)
