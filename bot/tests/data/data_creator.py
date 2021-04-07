import sys
import os

PACKAGE_PARENT = "../.."
SCRIPT_DIR = os.path.dirname(
    os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__)))
)
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

print(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from binance import binance_api, binance_config

import csv
import numpy

b_client = binance_api.BinanceAPI(binance_config.api_key, binance_config.api_secret)


try:
    symbol = sys.argv[1]
except IndexError:
    sys.exit("ERROR: Symbol argument missing")


try:
    """
    valid intervals: 1m 3m 5m 15m 30m 1h 2h 4h 6h 8h 12h 1d 3d 1w 1M
    """
    interval = sys.argv[2]
except IndexError:
    sys.exit("ERROR: Interval argument missing")


candles = b_client.get_klines_by_limit(symbol, interval, 1000)

if "msg" in candles:
    sys.exit("ERROR: " + candles["msg"])

data = [["close_time", "close", "high", "low", "open"]]
for candle in candles:
    data.append(
        [
            candle[6],
            numpy.double(candle[4]),
            numpy.double(candle[2]),
            numpy.double(candle[3]),
            numpy.double(candle[1]),
        ]
    )

with open("tests/data/" + symbol + ".csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(data)
