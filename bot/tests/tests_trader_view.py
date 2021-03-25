import pytest
from decimal import Decimal

from trader_view import get_sweet_spot_to_sell


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
