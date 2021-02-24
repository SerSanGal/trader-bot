from decimal import Decimal

import bot_config

def get_sweet_spot_to_buy(candle: list) -> dict:
    open_time = candle[0] # in milliseconds
    open_price = Decimal(candle[1]) 
    high_price = Decimal(candle[2]) 
    low_price = Decimal(candle[3]) 
    close_price = Decimal(candle[4]) 
    close_time = candle[6] # in milliseconds
    high_price = Decimal(candle[1]) 

    price = close_price * ( 1 - bot_config.profit )
    stop_limit_price = close_price * (1 + bot_config.tolerable_loss)

    return {
        "price": price_format(price),
        "stop_price": price_format(close_price),
        "stop_limit_price": price_format(stop_limit_price)
    }

def get_sell_range(buy_price, current_price):
    price = buy_price * (1 + bot_config.profit)
    stop_limit_price = buy_price * (1 - bot_config.tolerable_loss)
    return {
        "price": price_format(price),
        "stop_price": price_format(current_price),
        "stop_limit_price": price_format(stop_limit_price)
    }

def price_format(price: Decimal) -> str:
    return '{0:.8f}'.format(price)