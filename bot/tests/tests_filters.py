import pytest

from filters import filter_symbols_by_buy_coin, symbol_match


@pytest.mark.parametrize("symbol,coin,expected_output", [("ETHBTC", "BTC", True),("SUBBTC", "USDT", False),("SUBUSDT", "USDT", True)])
def test_symbol_match(symbol,coin,expected_output):
    actual_output = symbol_match(symbol, coin)
    assert actual_output == expected_output


def test_filter_symbols_by_buy_coin():
    event = ["SUBBTC", "SUBBUSD", "SUBUSDT", "SUBUSDC", "BTCUSDT", "USDTBTC"]
    expected_output = ["SUBUSDT", "BTCUSDT"]
    actual_output = filter_symbols_by_buy_coin(event, "USDT")
    assert actual_output == expected_output