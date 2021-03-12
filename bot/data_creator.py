import csv

import statistics
from decimal import Decimal

from binance_api import BinanceAPI
import binance_config

b_client = BinanceAPI(binance_config.api_key, binance_config.api_secret)


def create_data(symbol_info: dict):
    symbol = symbol_info["symbol"]
    candles = b_client.get_klines_by_limit(symbol, "12h", 730)

    fields = [
        symbol + "_open_time",
        symbol + "_open",
        symbol + "_high",
        symbol + "_low",
        symbol + "_close",
        symbol + "_volume",
        symbol + "_close_time",
        symbol + "_quote_asset_volume",
        symbol + "_number_of_trades",
        symbol + "_taker_buy_base_asset_volume",
        symbol + "_taker_buy_quote_asset_volume",
        symbol + "middle_bollinger_band",
        symbol + "upper_bollinger_band",
        symbol + "lower_bollinger_band",
    ]

    count = 0
    start_bollinger_band = 24 / 12 * 20
    last_20_candles = []
    plus_candles = []
    for candle in candles:
        candle.pop(len(candle) - 1)  # remove unusual value
        if count < start_bollinger_band:
            count = count + 1
            last_20_candles.append(candle)
            plus_candles.append(candle)
            continue

        standard_deviation = calculate_standard_deviation(last_20_candles)
        moving_20_candle = last_20_candles.pop(0)
        last_20_candles.append(candle)

        middle_bollinger_band = calculate_average_candle(moving_20_candle)
        upper_bollinger_band = middle_bollinger_band + (standard_deviation * 2)
        lower_bollinger_band = middle_bollinger_band - (standard_deviation * 2)

        candle.append(middle_bollinger_band)
        candle.append(upper_bollinger_band)
        candle.append(lower_bollinger_band)
        plus_candles.append(candle)

    rows = []
    for candle in plus_candles:
        rows.append(candle)

    with open("data/" + symbol + ".csv", "w") as f:
        write = csv.writer(f)
        write.writerow(fields)
        write.writerows(rows)


def calculate_average_candle(candle):
    high = Decimal(candle[2])
    low = Decimal(candle[3])
    return (high + low) / 2


def calculate_standard_deviation(last_20_candles):
    data = []
    for candle in last_20_candles:
        data.append(calculate_average_candle(candle))
    return statistics.stdev(data)


symbol_info = {"symbol": "BTCUSDT"}

create_data(symbol_info)

