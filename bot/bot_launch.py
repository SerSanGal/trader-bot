from multiprocessing import Process

import binance_api
import binance_config
import filters
from trader import start_trading


if __name__ == '__main__':
    b_client = binance_api.BinanceAPI(binance_config.api_key, binance_config.api_secret)

    exchange_info = b_client.get_exchange_info()
    symbols = [symbol["symbol"] for symbol in exchange_info["symbols"]]
    filtered_symbols = filters.filter_symbols_by_buy_coin(symbols, "USDT")

    print(len(filtered_symbols))

    list_of_process = []
    for symbol in filtered_symbols:
        p = Process(target=start_trading, args=(symbol,))
        p.name = symbol
        p.start()
        list_of_process.append({"process":p.name})
    print(list_of_process)







