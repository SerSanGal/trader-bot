import pytest
from decimal import Decimal

from trader_view import (
    get_sweet_spot_to_sell,
    bb_buy_signal,
    bb_dump_signal,
    rsi_buy_signal,
    rsi_dump_signal,
    storch_rsi_buy_signal,
    macd_buy_signal,
    storch_rsi_dump_signal,
    get_closes_from_candles,
    is_stable_coin,
    is_moving_up,
)
import numpy
import csv

import pandas_datareader.data as web


@pytest.mark.parametrize(
    "specs, expected_output",
    [
        (
            {
                "filters": [{"filterType": "PRICE_FILTER", "tickSize": "0.0010000",}],
                "executed_qty": Decimal(191.14),
                "current_price": Decimal(0.09500000),
                "cummulative_quote_qty": Decimal(20.012),
            },
            "0.105",
        ),
        (
            {
                "filters": [{"filterType": "PRICE_FILTER", "tickSize": "0.0010000",}],
                "executed_qty": Decimal(191.14),
                "current_price": Decimal(0.11500000),
                "cummulative_quote_qty": Decimal(20.012),
            },
            "0.115",
        ),
        (
            {
                "filters": [{"filterType": "PRICE_FILTER", "tickSize": "0.010000",}],
                "executed_qty": Decimal(191.14),
                "current_price": Decimal(0.11500000),
                "cummulative_quote_qty": Decimal(20.012),
            },
            "0.11",
        ),
    ],
)
def test_get_sweet_spot_to_sell(specs, expected_output):
    actual_output = get_sweet_spot_to_sell(specs)
    assert actual_output == expected_output


def get_data(symbol):
    data = []
    with open("tests/data/" + symbol + ".csv", newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=",", quotechar="|")
        next(reader, None)  # skip the headers
        for row in reader:
            data.append(numpy.double(row[1]))
    return numpy.array(data)


closes_1 = get_data("BTCUSDT")
closes_2 = get_data("SUPERUSDT")
closes_3 = get_data("FILUSDT")
closes_4 = get_data("MTLUSDT")
closes_5 = get_data("BUSDUSDT")


@pytest.mark.parametrize(
    "values, expected_output", [(closes_1, False,), (closes_2, True,)],
)
def test_bb_buy_signal(values, expected_output):
    actual_output = bb_buy_signal(values)
    assert actual_output == expected_output


@pytest.mark.parametrize(
    "values, expected_output", [(closes_3, True,), (closes_2, False,)],
)
def test_bb_dump_signal(values, expected_output):
    actual_output = bb_dump_signal(values)
    assert actual_output == expected_output


@pytest.mark.parametrize(
    "values, expected_output", [(closes_1, False,), (closes_4, True,)],
)
def test_rsi_buy_signal(values, expected_output):
    actual_output = rsi_buy_signal(values)
    assert actual_output == expected_output


@pytest.mark.parametrize(
    "values, expected_output", [(closes_1, False,), (closes_4, True,)],
)
def test_storch_rsi_buy_signal(values, expected_output):
    actual_output = storch_rsi_buy_signal(values)
    assert actual_output == expected_output


@pytest.mark.parametrize(
    "values, expected_output", [(closes_1, True,), (closes_4, False,)],
)
def test_macd_buy_signal(values, expected_output):
    actual_output = macd_buy_signal(values)
    assert actual_output == expected_output


@pytest.mark.parametrize(
    "values, expected_output", [(closes_3, True,), (closes_4, False,)],
)
def test_rsi_dump_signal(values, expected_output):
    actual_output = rsi_dump_signal(values)
    assert actual_output == expected_output


@pytest.mark.parametrize(
    "values, expected_output", [(closes_1, True,), (closes_4, False,)],
)
def test_storch_rsi_dump_signal(values, expected_output):
    actual_output = storch_rsi_dump_signal(values)
    assert actual_output == expected_output


@pytest.mark.parametrize(
    "values, expected_output", [(closes_5, True,), (closes_4, False,)],
)
def test_is_stable_coin(values, expected_output):
    actual_output = is_stable_coin(values)
    assert actual_output == expected_output


@pytest.mark.parametrize(
    "values, expected_output", [(closes_1, True,), (closes_4, False,)],
)
def test_is_moving_up(values, expected_output):
    actual_output = is_moving_up(values)
    assert actual_output == expected_output


def test_get_closes_from_candles():
    candles = [
        [
            1499040000000,  # Open time
            "0.01634790",  # Open
            "0.80000000",  # High
            "0.01575800",  # Low
            "0.01577100",  # Close
            "148976.11427815",  # Volume
            1499644799999,  # Close time
            "2434.19055334",  # Quote asset volume
            308,  # Number of trades
            "1756.87402397",  # Taker buy base asset volume
            "28.46694368",  # Taker buy quote asset volume
            "17928899.62484339",  # Ignore.
        ],
        [
            1499040000000,  # Open time
            "0.01634790",  # Open
            "0.80000000",  # High
            "0.01575800",  # Low
            "0.01677100",  # Close
            "148976.11427815",  # Volume
            1499644799999,  # Close time
            "2434.19055334",  # Quote asset volume
            308,  # Number of trades
            "1756.87402397",  # Taker buy base asset volume
            "28.46694368",  # Taker buy quote asset volume
            "17928899.62484339",  # Ignore.
        ],
    ]
    expected_output = numpy.array(
        [numpy.double("0.01577100"), numpy.double("0.01677100")]
    )
    actual_output = get_closes_from_candles(candles)
    assert numpy.all(actual_output == expected_output)
