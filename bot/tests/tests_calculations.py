import pytest

from calculations import price_format, get_sweet_spot_to_buy, get_sweet_spot_to_sell, is_bettable_symbol, join_candles

def test_price_format():
    price = 1
    expected_output = "1.00000000"
    actual_output = price_format(price)
    assert actual_output == expected_output

def test_get_sweet_spot_to_buy():
    event = [
    1499040000000,      # Open time
    "0.01634790",       # Open
    "0.80000000",       # High
    "0.01575800",       # Low
    "0.15771000",       # Close
    "148976.11427815",  # Volume
    1499644799999,      # Close time
    "2434.19055334",    # Quote asset volume
    308,                # Number of trades
    "1756.87402397",    # Taker buy base asset volume
    "28.46694368",      # Taker buy quote asset volume
    "17928899.62484339" # Ignore.
    ]
    expected_output = {
        "price": "0.15455580",
        "stop_price": "0.15771000",
        "stop_limit_price": "0.15928710"
    }

    actual_output = get_sweet_spot_to_buy(event)
    assert actual_output == expected_output


@pytest.mark.parametrize("buy_price,current_price,expected_output", [(1, 1.01, {
        "price": "1.02000000",
        "stop_price": "1.01000000",
        "stop_limit_price": "0.99000000"
    }),(1, 1.03, {
        "price": "1.03103000",
        "stop_price": "1.03000000",
        "stop_limit_price": "0.99000000"
    })])
def test_get_sweet_spot_to_sell(buy_price, current_price, expected_output):
    actual_output = get_sweet_spot_to_sell(buy_price, current_price)
    assert actual_output == expected_output



event_1 = [[
    1499040000000,      # Open time
    "0.16047900",       # Open
    "0.80000000",       # High
    "0.01575800",       # Low
    "0.17871000",       # Close
    "148976.11427815",  # Volume
    1499644799999,      # Close time
    "2434.19055334",    # Quote asset volume
    308,                # Number of trades
    "1756.87402397",    # Taker buy base asset volume
    "28.46694368",      # Taker buy quote asset volume
    "17928899.62484339" # Ignore.
    ]]
event_2 = [[
    1499040000000,      # Open time
    "0.1634790",       # Open
    "0.80000000",       # High
    "0.01575800",       # Low
    "0.15771000",       # Close
    "148976.11427815",  # Volume
    1499644799999,      # Close time
    "2434.19055334",    # Quote asset volume
    308,                # Number of trades
    "1756.87402397",    # Taker buy base asset volume
    "28.46694368",      # Taker buy quote asset volume
    "17928899.62484339" # Ignore.
    ]]
@pytest.mark.parametrize("candle,expected_output", [(event_1, True),(event_2, False)])
def test_is_bettable_symbol(candle, expected_output):
    actual_output = is_bettable_symbol(candle)
    assert actual_output == expected_output


def test_join_candles():
    candle1 = [
        101,
        "1",
        "10",
        "0.5",
        "8",
        "5",
        200,
        "7",
        2,
        "20",
        "30",
        "123456"
    ]
    candle2 = [
        201,
        "8",
        "15",
        "5",
        "21",
        "8",
        300,
        "9",
        6,
        "30",
        "40",
        "123458"
    ]
    candles = [candle1, candle2]
    expected_output = [
        101,
        "1",
        "15",
        "0.5",
        "21",
        "13",
        300,
        "16",
        8,
        "50",
        "70",
        0
    ]
    actual_output = join_candles(candles)
    assert actual_output == expected_output