from decimal import Decimal

# bot configuration

profit = Decimal(1 /100) # %
tolerable_loss = Decimal(0.5 / 100) # %

buy_tolerance_top = Decimal(0.95)
buy_tolerance_bottom = Decimal(1.05)

waiting_time_limit = 1 * 60 * 1000 # milliseconds