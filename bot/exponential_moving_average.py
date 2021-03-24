from decimal import Decimal


def calculate(candles: list, periode: int):
    EMA = [0] * (periode - 1)
    k_prices = []
    k = Decimal(2 / (1 + periode))
    count = 0
    for candle in candles:
        count += 1
        k_price = Decimal(candle[4]) * k
        k_prices.append(k_price)
        if count == periode:
            EMA.append(average(k_prices))
        if count > periode:
            last_EMA = EMA[len(EMA) - 1] * (1 - k)
            EMA.append(last_EMA + k_price)
    return EMA


def average(data: list) -> Decimal:
    return Decimal(sum(data) / len(data))

