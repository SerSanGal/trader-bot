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



def is_bettable_symbol(candle: list) -> bool:
    open_price = Decimal(candle[1])
    high_price = Decimal(candle[2])
    low_price = Decimal(candle[3])
    close_price = Decimal(candle[4]) 
    
    change_is_negative = open_price > close_price
    if change_is_negative:
        return False
    
    change = close_price/open_price
    amplitude = high_price/low_price
    #return amplitude
    
    if amplitude >= 1.03:
        return True
    else:
        return False
    