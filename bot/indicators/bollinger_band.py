from decimal import Decimal
import statistics


def calculate(values: list, periode=20) -> list:
    count = 0
    periode_values = []
    middle_bollinger_band = []
    upper_bollinger_band = []
    lower_bollinger_band = []
    for value in values:
        if count < periode:
            count = count + 1
            periode_values.append(value)
            continue

        standard_deviation = calculate_standard_deviation(periode_values)
        middle_bollinger_value = calculate_simple_moving_average(periode_values)

        periode_values.pop(0)
        periode_values.append(value)

        upper_bollinger_value = middle_bollinger_value + (standard_deviation * 2)
        lower_bollinger_value = middle_bollinger_value - (standard_deviation * 2)

        middle_bollinger_band.append(middle_bollinger_value)
        upper_bollinger_band.append(upper_bollinger_value)
        lower_bollinger_band.append(lower_bollinger_value)

    return {
        "MBB": middle_bollinger_band,
        "UBB": upper_bollinger_band,
        "LBB": lower_bollinger_band,
    }


def calculate_standard_deviation(periode_values):
    data = []
    for value in periode_values:
        data.append(Decimal(value))
    return statistics.stdev(data)


def calculate_simple_moving_average(periode_values):
    acc = 0
    for value in periode_values:
        acc += Decimal(value)
    return acc / len(periode_values)
