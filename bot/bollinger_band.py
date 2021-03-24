from decimal import Decimal
import statistics


def calculate(candles: list) -> list:
    count = 0
    start_bollinger_band = 20
    last_20_candles = []
    plus_candles = []
    for candle in candles:
        candle.pop(len(candle) - 1)  # remove unusual value
        if count < start_bollinger_band:
            count = count + 1
            last_20_candles.append(candle)
            plus_candles.append(candle)
            continue

        standard_deviation = calculate_standard_deviation(last_20_candles)
        middle_bollinger_band = calculate_simple_moving_average(last_20_candles)

        last_20_candles.pop(0)
        last_20_candles.append(candle)

        upper_bollinger_band = middle_bollinger_band + (standard_deviation * 2)
        lower_bollinger_band = middle_bollinger_band - (standard_deviation * 2)

        candle.append(middle_bollinger_band)
        candle.append(upper_bollinger_band)
        candle.append(lower_bollinger_band)
        plus_candles.append(candle)

    rows = []
    for candle in plus_candles:
        rows.append(candle)

    return rows[len(rows) - 1]


def calculate_standard_deviation(last_20_candles):
    data = []
    for candle in last_20_candles:
        data.append(Decimal(candle[4]))
    return statistics.stdev(data)


def calculate_simple_moving_average(last_20_candles):
    acc = 0
    for candle in last_20_candles:
        acc += Decimal(candle[4])  # close
    return acc / len(last_20_candles)