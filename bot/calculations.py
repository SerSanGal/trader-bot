from decimal import Decimal

import bot_config
import binance_config


def get_sweet_spot_to_sell(
    symbol_info: dict,
    executed_qty: Decimal,
    current_price: Decimal,
    cummulative_quote_qty: Decimal,
) -> dict:

    tick_size = symbol_tick_size(symbol_info["filters"])

    bet = cummulative_quote_qty


    price = bet * (1 + bot_config.profit) * (1 + binance_config.fee) / executed_qty

    if current_price >= price:
        price = current_price * (1 + Decimal(tick_size))
        stop_limit_price = current_price * (1 - Decimal(tick_size))
    else: 
        stop_limit_price = (
            bet * (1 - bot_config.tolerable_loss) * (1 + binance_config.fee) / executed_qty
        )

    if stop_limit_price >= current_price:
        stop_limit_price = current_price * (1 - Decimal(tick_size))

    stop_price = stop_limit_price

    return {
        "current_price": current_price,
        "price": price_format(price, tick_size),
        "stop_price": price_format(stop_price, tick_size),
        "stop_limit_price": price_format(stop_limit_price, tick_size),
    }


def is_correct_lot_size(filters: list, quantity: Decimal) -> int:
    """
        Decide if the quantity is fit with the lot size 
        filter of the symbol.
        
        Parameters
        ----------
        filters : list of symbol filters, mandatory

        Return
        ------
        correct quantity : int
            0 : the quantity is correct
            1 : the quantity is too high
           -1 : the quantity is too low 
            None : LOT_SIZE filter does not found in filters
    """
    for filter in filters:
        if filter["filterType"] == "LOT_SIZE":
            if Decimal(filter["minQty"]) > quantity:
                return -1
            elif Decimal(filter["maxQty"]) < quantity:
                return 1
            else:
                return 0
    return


def symbol_tick_size(filters: list) -> str:
    for filter in filters:
        if filter["filterType"] == "PRICE_FILTER":
            return filter["tickSize"]


def symbol_quantity_step_size(filters: list) -> int:
    for filter in filters:
        if filter["filterType"] == "LOT_SIZE":
            return filter["stepSize"].find("1") - 1


def price_format(price: Decimal, tick_size: int) -> str:
    return "{:.{prec}f}".format(price, prec=tick_size.find("1") - 1)


def quantity_format(quantity: Decimal, step_size: int) -> Decimal:
    return Decimal("{:.{prec}f}".format(quantity, prec=step_size))


def candle_quality(candle: list, threshold) -> bool:
    """
        Decide if a candle is good enough.

        The function wait a candle. It compare the open and close points
        to determine if this candle is good.

        the change in % is compared to a % threshold.
        
        Parameters
        ----------
        candle : a candle, mandatory
            symbol candle.

        Return
        ------
        is_candle_good : bool
            True: is a good candle
            False: is not a good candle
    """
    open_price = Decimal(candle[1])
    high_price = Decimal(candle[2])
    low_price = Decimal(candle[3])
    close_price = Decimal(candle[4])

    if open_price > close_price:
        return False

    change = close_price / open_price
    # amplitude = high_price / low_price

    is_candle_good = change >= threshold

    if is_candle_good:
        return True
    else:
        return False


def is_bettable_symbol(candles: list) -> bool:
    """
        Decide if a symbol is a good candidate from a list of candles.

        The function wait a list of 15 or more candles of 
        1m limit time. 

        First it check if the whole candles are positive. If then candle
        is negative, it will return the symbol is not a good candidate.

        If the whole candles are positive it will check if the whole candle
        increment is big enough. 
        
        If incremente is big enough it will check the increment of the last 
        2 minutes, i.e. the last to candles. 
        
        Parameters
        ----------
        candles : candle list, mandatory
            symbol candles. The function wait a list of 15 or more candles of 
            1m limit time.

        Return
        ------
        bettable_symbol : bool
            True: is a good candidate to bet
            False: is not good enough to bet
    """
    try:
        whole_candles = join_candles(candles)
        is_whole_candles_good = candle_quality(
            whole_candles, 1.08
        )  # see global candel state
        if not is_whole_candles_good:
            return False

        last_candles = join_candles(candles[len(candles) - 2 :])
        is_last_candles_good = candle_quality(
            last_candles, 1.05
        )  # see global candel state
        if not is_last_candles_good:
            return False

        is_last_candle_good = candle_quality(candles[len(candles) - 1], 1)

        if is_last_candle_good:
            return True
        else:
            return False
    except:
        print("An exception occurred in is_bettable_symbol")
        print(candles)
        return False


def join_candles(candles: list) -> list:
    open_time = candles[0][0]
    open_price = candles[0][1]
    high_price = max([candle[2] for candle in candles])
    low_price = min([candle[3] for candle in candles])
    close_price = candles[len(candles) - 1][4]
    volume = str(sum([Decimal(candle[5]) for candle in candles]))
    close_time = candles[len(candles) - 1][6]
    quote_asset_volume = str(sum([Decimal(candle[7]) for candle in candles]))
    number_of_trades = int(sum([Decimal(candle[8]) for candle in candles]))
    taker_buy_base = str(sum([Decimal(candle[9]) for candle in candles]))
    taker_buy_quote = str(sum([Decimal(candle[10]) for candle in candles]))
    ignore = 0

    joined_candles = [
        open_time,
        open_price,
        high_price,
        low_price,
        close_price,
        volume,
        close_time,
        quote_asset_volume,
        number_of_trades,
        taker_buy_base,
        taker_buy_quote,
        ignore,
    ]

    return joined_candles

