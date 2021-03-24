from decimal import Decimal


def calculate(values: list, periode: int):
    EMA = []
    k_prices = []
    k = Decimal(2 / (1 + periode))
    count = 0
    for value in values:
        count += 1
        k_price = Decimal(value) * k
        k_prices.append(k_price)
        if count == periode:
            EMA.append(average(values[0:periode]))
        if count > periode:
            last_EMA = EMA[len(EMA) - 1] * (1 - k)
            EMA.append(last_EMA + k_price)
    
    return EMA


def average(data: list) -> Decimal:
    return Decimal(sum(data) / len(data))