from multiprocessing import Process

import binance_api
import binance_config
import filters
import bot_config
from data_creator import create_data
import time
from decimal import Decimal

from datetime import datetime

if __name__ == "__main__":
    b_client = binance_api.BinanceAPI(binance_config.api_key, binance_config.api_secret)

    exchange_info = b_client.get_exchange_info()
    symbols = [symbol for symbol in exchange_info["symbols"]]
    filtered_symbols = filters.filter_symbols_by_buy_coin(symbols, bot_config.coin)

    filtered_symbol_by_spec = filters.filter_by_spec(filtered_symbols)

    print("Number of data creators", len(filtered_symbol_by_spec))

    list_of_process = []
    for symbol in filtered_symbol_by_spec:
        p = Process(target=create_data, args=(symbol,))
        p.name = symbol["symbol"]
        p.start()
        list_of_process.append({"process": p.name})
    # print(list_of_process)

