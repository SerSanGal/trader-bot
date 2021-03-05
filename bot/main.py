import binance_api
import binance_config
import calculations
import filters
import time
from datetime import datetime
import trader

b_client = binance_api.BinanceAPI(binance_config.api_key, binance_config.api_secret)

exchange_info = b_client.get_exchange_info()
symbols = [symbol["symbol"] for symbol in exchange_info["symbols"]]
filtered_symbols = filters.filter_symbols_by_buy_coin(symbols, "USDT")

print(len(filtered_symbols))

quantity = 10 # USDT

while True:

    bettable_symbols = []
    count = 0
    for symbol in filtered_symbols:
        candles = b_client.get_klines_by_limit(symbol, "1m", 5)
        is_candidate = calculations.is_bettable_symbol(candles)
        #print(symbol, is_candidate)
        
        if is_candidate:
            bettable_symbols.append(symbol)
            print(datetime.now(),symbol)
            #trader.trading(b_client, symbols, quantity, candles[0])
        
        #time.sleep(1)
    print("Round finished at: ", datetime.now())
    #print(datetime.now(),bettable_symbols)

