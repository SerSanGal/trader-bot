
from decimal import Decimal


def calculate(values: list, periode=14) -> list:
    if(len(values)<periode):
        return "ERROR"
    relative_strength_indexes = []
    for c in reversed(range(0 , len(values), periode)):
        average_upward_prices = []
        average_downward_prices = []
        for i in reversed(range(1, periode)):
            ic = i + c
            diff = values[ic] - values[ic-1]
            if diff < 0:
                average_downward_prices.append(abs(diff))
            else:
                average_upward_prices.append(diff)
    
        average_upward_price_change = sum(average_upward_prices)/periode
        average_downward_price_change = sum(average_downward_prices)/periode
        
        relative_strength = average_upward_price_change/average_downward_price_change
        relative_strength_index = 100 - (100/(1+relative_strength))
        relative_strength_indexes.append(relative_strength_index)
    
    return relative_strength_indexes