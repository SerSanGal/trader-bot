def filter_symbols_by_buy_coin(symbols: list, coin: str) -> list:
    return [symbol for symbol in symbols if symbol_match(symbol, coin)]


def symbol_match(symbol: str, coin: str) -> bool:
    sell_coin = symbol[0 : len(symbol) - len(coin)]
    if discard_special_coins(sell_coin):
        return False

    buy_coin = symbol[len(symbol) - len(coin) :]
    return buy_coin == coin


def discard_special_coins(coin: str) -> bool:
    special_coins = ["UP", "DOWN"]
    if any(
        special_coin for special_coin in special_coins if coin.find(special_coin) != -1
    ):
        return True
    else:
        return False
