from datetime import datetime
from calculations import get_sweet_spot_to_buy, get_sell_range


def trading(symbol: str, quantity: str):
    buy_configuration = get_buy_configuration(symbol)
    buy_oco_order = oco_order(symbol, "buy", buy_configuration, quantity)
    buy_oco_order_time = datetime.now()
    
    buy_oco_result = oco_order_control(buy_oco_order, buy_oco_order_time)


    sell_configuration = get_sell_configuration(buy_oco_result)
    sell_oco_order = oco_order(symbol, "sell", sell_configuration, symbol_bought_quantity)
    sell_oco_order_time = datetime.now()

    oco_order_control(sell_oco_order, sell_oco_order_time)
    
    if is_symbol_good_to_trading(symbol):
        quantity = get_bet_quantity()
        trading(symbol, quantity)
    else:
        return


def oco_order_control(oco_order: dict, oco_order_time: int) -> dict:
    while True:
        now = datetime.now()
        order_status = check_oco_status(oco_order)
        if order_status != "EXECUTING":
            order = get_order_from_order_list_id(oco_order["orderListId"])
            break

        elif (now - oco_order_time) > bot_config.waiting_time_limit:
            cancel_oco_order(oco_order)
            break
    
    return order


def cancel_oco_order(oco_order: dict):
    # if oco_order is a buyer order, just cancel the order
    # if oco_order is a seller order, sell to the market price
    # TODO: call api endpoint
    return


def get_sell_configuration(order: dict) -> dict:
    current_price = get_current_price(order['symbol'])
    return get_sell_range(order['price'], current_price)

def get_order_from_order_list_id(order_list_id: int) -> dict:
    # TODO: call api endpoint
    return


def get_buy_configuration(symbol: str) -> dict:
    candle = get_candle(symbol, "1m", 2)
    return get_sweet_spot_to_buy(candle)




def check_oco_status(oco_order: dict) -> str:
    # TODO: call api endpoint
    return


def oco_order(symbol: str, side: str, sell_configuration: dict, quantity: str) -> dict:
    # TODO: call api endpint
    return


def get_current_price(symbol: str):
    # TODO: call api endpint
    return


def get_candle(symbol: str, interval: str, number_of_intervals: int) -> list:
    return

def is_symbol_good_to_trading(symbol: str) -> bool:
    return

def get_bet_quantity() -> str:
    return