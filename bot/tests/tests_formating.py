import pytest
from decimal import Decimal

from formating import (
    price_format,
    is_correct_lot_size,
    symbol_tick_size,
    symbol_quantity_step_size,
    quantity_format,
)

# TODO: (Decimal(11.99),"10","10"),
@pytest.mark.parametrize(
    "input_price,tick_size,output_price",
    [
        (Decimal(1.992345678), "1", "1"),
        (Decimal(1.19345678), "0.1", "1.1"),
        (Decimal(1.12945678), "0.01", "1.12"),
        (Decimal(1.12365678), "0.001", "1.123"),
        (Decimal(1.12346678), "0.0001", "1.1234"),
    ],
)
def test_price_format(input_price, tick_size, output_price):
    actual_output = price_format(input_price, tick_size)
    assert actual_output == output_price


@pytest.mark.parametrize(
    "filters, quantity, expected_output",
    [
        (
            [
                {
                    "filterType": "LOT_SIZE",
                    "minQty": "0.00100000",
                    "maxQty": "100000.00000000",
                }
            ],
            Decimal(1),
            0,
        ),
        (
            [
                {
                    "filterType": "LOT_SIZE",
                    "minQty": "1.00000000",
                    "maxQty": "100000.00000000",
                }
            ],
            Decimal(0.1),
            -1,
        ),
        (
            [
                {
                    "filterType": "LOT_SIZE",
                    "minQty": "0.00100000",
                    "maxQty": "100.00000000",
                }
            ],
            Decimal(101),
            1,
        ),
    ],
)
def test_is_correct_lot_size(filters, quantity, expected_output):
    actual_output = is_correct_lot_size(filters, quantity)
    assert actual_output == expected_output


def test_symbol_tick_size():
    filters = [
        {
            "filterType": "PRICE_FILTER",
            "tickSize": "0.00000100",
        }
    ]
    expected_output = "0.00000100"
    actual_output = symbol_tick_size(filters)
    assert actual_output == expected_output


@pytest.mark.parametrize(
    "filters, expected_output",
    [
        (
            [
                {
                    "filterType": "LOT_SIZE",
                    "stepSize": "1.00000000",
                }
            ],
            0,
        ),
        (
            [
                {
                    "filterType": "LOT_SIZE",
                    "stepSize": "0.10000000",
                }
            ],
            1,
        ),
        (
            [
                {
                    "filterType": "LOT_SIZE",
                    "stepSize": "0.00100000",
                }
            ],
            3,
        ),
    ],
)
def test_symbol_quantity_step_size(filters, expected_output):
    actual_output = symbol_quantity_step_size(filters)
    assert actual_output == expected_output
    

@pytest.mark.parametrize(
    "quantity,step_size,expected_output",
    [
        (Decimal(1.992345678), 0, Decimal(1)),
        (Decimal(1.19345678), 1, Decimal("{:.1f}".format(1.1))),
        (Decimal(1.12945678), 2, Decimal("{:.2f}".format(1.12))),
    ],
)
def test_quantity_format(quantity, step_size, expected_output):
    actual_output = quantity_format(quantity, step_size)
    assert actual_output == expected_output