from datetime import datetime
from calculations import (
    get_sweet_spot_to_buy,
    get_sweet_spot_to_sell,
    is_bettable_symbol,
)
from binance_api import BinanceAPI
import bot_config
import time


def trading(client: BinanceAPI, symbol: str, bet: str, candle: list):
    global b_client
    b_client = client
    sweet_spot_to_buy = get_sweet_spot_to_buy(candle[0])
    # TODO: calculcate quantity from bet and the stop limit price
    quantity_to_buy = bet / sweet_spot_to_buy["stop_limit_price"]
    buy_oco_order = b_client.buy_oco(symbol, quantity_to_buy, sweet_spot_to_buy)
    buy_oco_order_time = datetime.now()

    buy_oco_result = oco_order_control(buy_oco_order, buy_oco_order_time)
    if buy_oco_result == "CANCELLED" or buy_oco_result == "REJECT":
        return

    sweet_spot_to_sell = get_sell_configuration(buy_oco_result)
    quantity_to_sell = buy_oco_result["executedQty"]
    sell_oco_order = b_client.sell_oco(symbol, quantity_to_sell, sweet_spot_to_sell)
    sell_oco_order_time = datetime.now()

    sell_oco_result = oco_order_control(sell_oco_order, sell_oco_order_time)
    if sell_oco_result == "CANCELLED" or sell_oco_result == "REJECT":
        return

    candles = b_client.get_klines_by_limit(symbol, "15m", 1)
    is_candidate = is_bettable_symbol(candles[0])
    if is_candidate:
        bet = get_bet()
        trading(b_client, symbol, bet, candles[0])
    else:
        return


def oco_order_control(oco_order: dict, oco_order_time: int) -> dict:
    while True:
        now = datetime.now()
        order_status = check_oco_status(oco_order)
        if order_status == "EXECUTING":
            if (now - oco_order_time) > bot_config.waiting_time_limit:
                cancel_oco_order(oco_order)
                order = "CANCELLED"
                break
        elif order_status == "ALL_DONE":
            order = get_finished_order_from_oco_order(oco_order)
            break
        elif order_status == "REJECT":
            # TODO: check reject reason
            order = order_status
            break
        time.sleep(1)

    return order


def cancel_oco_order(oco_order: dict):
    # if oco_order is a buyer order, just cancel the order
    # if oco_order is a seller order, sell to the market price
    # TODO: call api endpoint
    return


def get_sell_configuration(order: dict) -> dict:
    cummulative_quote_qty = order["cummulativeQuoteQty"]
    current_price = b_client.get_symbol_price(order["symbol"])["price"]
    return get_sweet_spot_to_sell(cummulative_quote_qty, current_price)


def get_finished_order_from_oco_order(oco_order: dict) -> dict:
    for order in oco_order["orders"]:
        order_detail = b_client.query_order(order["symbol"], order["orderId"])
        if order_detail["status"] == "FILLED":
            return order_detail


def check_oco_status(oco_order: dict) -> str:
    result = b_client.query_oco_order(oco_order["orderListId"])
    return result["listOrderStatus"]


def oco_order(symbol: str, side: str, configuration: dict, quantity: str) -> dict:
    # TODO: call api endpint
    return


def get_current_price(symbol: str):
    # TODO: call api endpint
    return


def get_candle(symbol: str, interval: str, number_of_intervals: int) -> list:
    return


def is_symbol_good_to_trading(symbol: str) -> bool:
    return


def get_bet() -> str:
    return "10"


"""
bet = 1000 usdt + 0.2 / + 0

price = 9,7
stopPrice = 9,9 --> actual price
stopLimitPrice = 10

quantity = 100 

10,2

"""

