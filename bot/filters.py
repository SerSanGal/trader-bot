

def filter_symbols_by_buy_coin(symbols: list, coin: str) -> list:
    return [symbol for symbol in symbols if symbol_match(symbol, coin)]


def symbol_match(symbol: str, coin: str) -> bool:
    return symbol[len(symbol)-len(coin):] == coin