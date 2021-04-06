import bot_config
from decimal import Decimal

from binance import binance_config
from formating import symbol_tick_size, price_format

from talib import BBANDS, RSI, MA, STOCHRSI, MACD
import numpy


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


def is_a_buy_signal(closes):
    if storch_rsi_buy_signal(closes) and bb_buy_signal(closes):
        return True
    else:
        return False


def is_moving_up(closes: list) -> bool:
    ma_last = ma(closes)[-1]
    return ma_last < closes[-1]


def bb_buy_signal(closes: list) -> bool:
    bbp_last = bbp(closes)[-1]
    return bbp_last < 0


def rsi_buy_signal(closes: list) -> bool:
    rsi_last = rsi(closes)[-1]
    return rsi_last < 30


def storch_rsi_buy_signal(closes: list) -> bool:
    storch_rsi_last = storch_rsi(closes)[-1]
    return storch_rsi_last < 20


def macd_buy_signal(closes: list) -> bool:
    macd_hist_last = macd_hist(closes)[-1]
    return macd_hist_last > 0


def bb_dump_signal(closes: list) -> bool:
    bbp_last = bbp(closes)[-1]
    return bbp_last > 1


def rsi_dump_signal(closes: list) -> bool:
    rsi_last = rsi(closes)[-1]
    return rsi_last > 70


def storch_rsi_dump_signal(closes: list) -> bool:
    storch_rsi_last = storch_rsi(closes)[-1]
    return storch_rsi_last > 80


def is_stable_coin(closes: list) -> bool:
    stability = abs(((abs(numpy.std(closes)) + closes[-1]) / closes[-1]) - 1)
    return stability < 0.005


def ma(closes: list) -> list:
    return MA(closes, timeperiod=60)


def bb(closes: list) -> list:
    return BBANDS(closes, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)


def bbp(closes: list) -> list:
    up, mid, low = bb(closes)

    a = closes - low
    b = up - low

    bbp = numpy.divide(a, b, out=numpy.zeros_like(a), where=b != 0)
    return bbp


def rsi(closes: list) -> list:
    return RSI(closes, timeperiod=14)


def storch_rsi(closes: list) -> list:
    fastk, fastd = STOCHRSI(
        closes, timeperiod=14, fastk_period=5, fastd_period=3, fastd_matype=0
    )
    return fastk


def macd_hist(closes: list) -> list:
    macd, macdsignal, macdhist = MACD(
        closes, fastperiod=12, slowperiod=26, signalperiod=9
    )
    return macdhist


def get_closes_from_candles(candles: list) -> list:
    closes = []
    for candle in candles:
        closes.append(numpy.double(candle[4]))
    return numpy.array(closes)


#  ----- OLD ------
def is_bull_trend(candles: list, periode=60) -> bool:
    closes = [candle[4] for candle in candles]
    last_close = closes[-1]
    MA = sum(closes[-periode]) / periode
    return last_close > MA


def is_a_dip(candles: list) -> bool:
    closes = [candle[4] for candle in candles]
    last_close = closes[-1]
    up, mid, low = BBANDS(closes, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
    last_lower_bollinger_value = low[-1]
    if Decimal(last_close) < Decimal(last_lower_bollinger_value):
        return True
    else:
        return False


def is_a_buy_zone(candles: list) -> bool:
    closes = [candle[4] for candle in candles]
    last_close = closes[-1]
    up, mid, low = BBANDS(closes, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
    last_lower_bollinger_value = low[-1]
    if Decimal(last_close) > Decimal(last_lower_bollinger_value):
        return True
    else:
        return False

