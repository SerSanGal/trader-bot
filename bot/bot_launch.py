from multiprocessing import Process

from binance import binance_api, binance_config
import filters
import bot_config
from trader import start_trading
import time
from decimal import Decimal

from datetime import datetime

if __name__ == "__main__":
    b_client = binance_api.BinanceAPI(binance_config.api_key, binance_config.api_secret)
    try:
        exchange_info = b_client.get_exchange_info()
        if "msg" in exchange_info:
            print("bot_launch", "EXCHANGE INFO ERROR", exchange_info["msg"])
            exit()
    except:
        print("bot_launch", "API ERROR")
        exit()
    
    symbols = [symbol for symbol in exchange_info["symbols"]]
    filtered_symbols = filters.filter_symbols_by_buy_coin(symbols, bot_config.coin)

    filtered_symbol_by_spec = filters.filter_by_spec(filtered_symbols)

    print("Number of bots launched", len(filtered_symbol_by_spec))

    list_of_process = []
    for symbol in filtered_symbol_by_spec:
        p = Process(target=start_trading, args=(symbol,))
        p.name = symbol["symbol"]
        p.start()
        list_of_process.append({"process": p.name})
    # print(list_of_process)

    while True:
        try:
            account = b_client.get_account()
            if "msg" in account:
                print("bot_launch", "ACCOUNT ERROR", account["msg"])
                time.sleep(60)
                continue
        except:
            print("bot_launch", "API ERROR")
            time.sleep(60)
            continue
        
        total = 0
        for coin in account["balances"]:
            if coin["asset"] != bot_config.coin and (
                Decimal(coin["free"]) > 0 or Decimal(coin["locked"]) > 0
            ):
                symbol = coin["asset"] + bot_config.coin
                symbol_price = Decimal(b_client.get_symbol_price(symbol)["price"])
            else:
                symbol_price = 1
            total = (
                total + (Decimal(coin["free"]) + Decimal(coin["locked"])) * symbol_price
            )
        print(datetime.now(), total) 
        with open('history.csv','a') as fd:
            fd.write(str(datetime.now()) + ", " + str(total) + "\n")
        time.sleep(60)
