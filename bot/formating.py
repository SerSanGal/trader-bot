from decimal import Decimal
import math
import numpy


def price_format(price: Decimal, tick_size: str) -> str:
    prec = tick_size.find("1") - 1
    if prec < 0:
        return "{}".format(int(price))
    else:
        multiplier = Decimal(math.pow(10, prec))
        price = Decimal(int(price * multiplier) / multiplier)
        return "{:.{prec}f}".format(price, prec=prec)


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
            prec = filter["stepSize"].find("1") - 1
            if prec < 0:
                return 0
            else:
                return prec


def quantity_format(quantity: Decimal, step_size: int) -> Decimal:
    if step_size == 0:
        return Decimal("{}".format(int(quantity)))
    else:
        multiplier = Decimal(math.pow(10, step_size))
        quantity = Decimal(int(quantity * multiplier) / multiplier)
        return Decimal("{:.{prec}f}".format(quantity, prec=step_size))


def sanitize_candle_for_pattern_recognition(candles: list) -> dict:
    input_data = {
        "close_time": [],
        "open": [],
        "high": [],
        "low": [],
        "close": [],
    }
    for candle in candles:
        input_data["close_time"].append(numpy.double(candle[6]))
        input_data["close"].append(numpy.double(candle[4]))
        input_data["high"].append(numpy.double(candle[2]))
        input_data["low"].append(numpy.double(candle[3]))
        input_data["open"].append(numpy.double(candle[1]))

    data = {}
    data["close_time"] = numpy.array(input_data["close_time"])
    data["close"] = numpy.array(input_data["close"])
    data["high"] = numpy.array(input_data["high"])
    data["low"] = numpy.array(input_data["low"])
    data["open"] = numpy.array(input_data["open"])
    return data
