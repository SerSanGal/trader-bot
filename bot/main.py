import binance_api
import binance_config
import calculations
import filters
import time
import trader

b_client = binance_api.BinanceAPI(binance_config.api_key, binance_config.api_secret)

exchange_info = b_client.get_exchange_info()
symbols = [symbol["symbol"] for symbol in exchange_info["symbols"]]
filtered_symbols = filters.filter_symbols_by_buy_coin(symbols, "USDT")

print(len(filtered_symbols))

quantity = 10 # USDT

# while true:

bettable_symbols = []
count = 0
for symbol in filtered_symbols:
    candles = b_client.get_klines_by_limit(symbol, "15m", 1)
    is_candidate = calculations.is_bettable_symbol(candles[0])
    print(symbol, is_candidate)
    
    if is_candidate:
        bettable_symbols.append(symbol)
        trader.trading(b_client, symbols, quantity, candles[0])
    
    time.sleep(1)

print(bettable_symbols)

