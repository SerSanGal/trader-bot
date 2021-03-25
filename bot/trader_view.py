import bot_config
from decimal import Decimal
from indicators import bollinger_band

from binance import binance_config
from formating import symbol_tick_size, price_format


def get_sweet_spot_to_sell(specs: dict) -> dict:
    filters = specs["filters"]
    executed_qty = specs["executed_qty"]
    current_price = specs["current_price"]
    cummulative_quote_qty = specs["cummulative_quote_qty"]

    tick_size = symbol_tick_size(filters)

    bet = cummulative_quote_qty

    price = bet * (1 + bot_config.profit) * (1 + binance_config.fee) / executed_qty

    if current_price >= price:
        price = current_price * (1 + Decimal(tick_size))

    return price_format(price, tick_size)


def there_is_hype(candles: list) -> bool:
    closes = [candle[4] for candle in candles]
    last_close = closes[-1]
    bb = bollinger_band.calculate(closes)

    is_up = Decimal(last_close) > Decimal(bb["UBB"][-1])

    is_volatile = (
        Decimal(bb["UBB"]) / Decimal(bb["LBB"][-1]) - 1
    ) > 5 * bot_config.profit

    if is_up and is_volatile:
        return is_bull_trend(candles)
    else:
        return False


def is_bull_trend(candles: list, periode=60) -> bool:
    closes = [candle[4] for candle in candles]
    last_close = closes[-1]
    MA = sum(closes[-periode]) / periode
    return last_close > MA


def is_a_dip(candles: list) -> bool:
    closes = [candle[4] for candle in candles]
    last_close = closes[-1]
    bb = bollinger_band.calculate(closes)
    last_lower_bollinger_value = bb["LBB"][-1]
    if Decimal(last_close) < Decimal(last_lower_bollinger_value):
        return True
    else:
        return False


def is_a_buy_zone(candles: list) -> bool:
    closes = [candle[4] for candle in candles]
    last_close = closes[-1]
    bb = bollinger_band.calculate(closes)
    last_lower_bollinger_value = bb["LBB"][-1]
    if Decimal(last_close) > Decimal(last_lower_bollinger_value):
        return True
    else:
        return False

