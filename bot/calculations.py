from decimal import Decimal

import bot_config


def get_sweet_spot_to_buy(candle: list) -> dict:
    # open_time = candle[0] # in milliseconds
    # open_price = Decimal(candle[1]) 
    # high_price = Decimal(candle[2]) 
    # low_price = Decimal(candle[3]) 
    close_price = Decimal(candle[4]) 
    # close_time = candle[6] # in milliseconds
    # high_price = Decimal(candle[1]) 

    price = close_price * bot_config.buy_tolerance_top
    stop_limit_price = close_price * bot_config.buy_tolerance_bottom

    return {
        "price": price_format(price),
        "stop_price": price_format(close_price),
        "stop_limit_price": price_format(stop_limit_price),
    }

def get_sweet_spot_to_sell(purchase_price: str, current_price: str) -> dict:
    price = Decimal(purchase_price) * (1 + bot_config.profit)
    if Decimal(current_price) > price:
        price = Decimal(current_price) * Decimal(1.001)
        
    stop_limit_price = Decimal(purchase_price) * (1 - bot_config.tolerable_loss)
    return {
        "price": price_format(price),
        "stop_price": price_format(Decimal(current_price)),
        "stop_limit_price": price_format(stop_limit_price)
    }

def price_format(price: Decimal) -> str:
    return '{0:.8f}'.format(price)


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
    
    change_is_negative = open_price > close_price
    if change_is_negative:
        return False
    
    #change = close_price / open_price
    amplitude = high_price/low_price

    is_candle_good = amplitude >= threshold

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
    whole_candles = join_candles(candles)
    is_whole_candles_good = candle_quality(
        whole_candles, 1.03
    )  # see global candel state
    if not is_whole_candles_good:
        return False

    last_candles = join_candles(candles[len(candles) - 2 :])
    is_last_candles_good = candle_quality(last_candles, 1.0175)  # see global candel state
    if not is_last_candles_good:
        return False
    
    is_last_candle_good = candle_quality(candles[len(candles) - 1], 1) 
    
    if is_last_candle_good:
        return True
    else:
        return False
    