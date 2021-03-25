from indicators.relative_strength_index import calculate as rsi
from decimal import Decimal


def test_rsi():
    values = [6.02, 5.95, 5.95, 5.98, 5.83, 5.81, 5.86, 6.06, 6.09]
    periode = 9
    expected_output = 56.36
    actual_output = int(100*rsi(values, periode)[0])/100
    assert actual_output == expected_output
