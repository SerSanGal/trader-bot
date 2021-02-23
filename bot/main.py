import time

results = []
# TODO: Get all open orders from Binance, in case that the program was previously closed.
while True:
  symbols_info = get_symbols_statistics_24hr() # List
  balance = get_balance() # $100 in binance
  risk_factor = 0.01 # % you are willing to bet 1% of $100 in balance 
  bettable_coins = compose(
    filterByPriceChange(0.3, '24 hours'),
    discardNewbornCoins,
    filterByPriceChange(0.2, '4 hours'),
    filterByPriceChange(0.15, '1 hours'),
  )
  bet_quantity = calculate_bet_quantity(balance, risk_factor)  # ($100, 0.01) -> $1 is the bet quantity
  bets_in_progress = get_bets_in_progress(results)
  bettable_slots = max(calculate_number_of_bets(balance, bet_quantity, bets_in_progress)), len(bettable_coins)) # max((100 / 2) / 1), len(["BTC", "ETH", "DOGE"])) = 3 bettable slots
  
  # TODO: when you have more bettable coins than slots, pick the "best" coins. Best is ???
  best_coins = pick_best_coins(bettable_coins, bettable_slots)
  
  # ~sort of bet function~
  for slot, coin in zip(bettable_slots, best_coins):
    buy_result = buy(coin, "market_price") # buys 1$ worth of [BTC, ETH...]
    results[coin][order_id]["buyResult"] = buy_result
    results[coin][order_id]["status"] = "progress"

    profit = 0.02
    price = bet_quantity * (1 + profit)
    stop_price = bet_quantity
    stop_limit_price = bet_quantity * (1 + (profit / 2))
    timestamp = int(time.time * 1000)
    sell_result = sell(coin, price, stop_price, stop_limit_price, order_id, timestamp)
    results[coin][order_id]["sellResult"] = sell_result

  for bet_in_progress in bets_in_progress:
    order_list_id = bet_in_progress["orderListId"]
    timestamp = int(time.time() * 1000)
    bet_data = get_bet_data(order_list_id, timestamp)
    bet_transaction_time = bet_data["transactionTime"]
    bet_status = bet_data["listOrderStatus"]
    symbol = bet_data["symbol"]

    if bet_status == "FINISHED":
      order_id = bet_data["listClientOrderId"]
      results[symbol][order_id]["status"] = "finished"
    else:
      threshold_limit_in_milliseconds = 30 * 60 * 1000
      bet_timestamp = bet_data["transactionTime"]
      now = int(time.time() * 1000)

      if bet_timestamp + threshold_limit_in_milliseconds < now:
        cancel_bet(symbol, order_list_id, now)
