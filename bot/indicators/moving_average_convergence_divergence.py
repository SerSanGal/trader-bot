import exponential_moving_average as EMA


def calculate(values: list, periode_1=12, periode_2=26, signal_periode=9) -> dict:
    if len(values) < periode_2:
        return "ERROR"

    if periode_2 < periode_1:
        return "ERROR"

    EMA_1 = [0] * (periode_1 - 2) + EMA.calculate(values, periode_1)
    EMA_2 = [0] * (periode_2 - 2) + EMA.calculate(values, periode_2)

    aux_MACD = [abs(x - y) for x, y in zip(EMA_1, EMA_2) if y != 0]
    aux_signal = EMA.calculate(aux_MACD, signal_periode + 1)
    
    MACD = [0] * periode_2 + aux_MACD
    signal = [0] * (periode_2 + signal_periode) + aux_signal
    
    aux_histogram = [x - y for x, y in zip(MACD, signal) if y != 0]
    
    histogram = [0] * (periode_2 + signal_periode) + aux_histogram

    return {
        "MACD": MACD,
        "signal": signal,
        "histogram": histogram,
    }

