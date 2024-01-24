from config_execution_api import stop_loss_fail_safe
from config_execution_api import ticker_1
from config_execution_api import ticker_2
from config_execution_api import price_rounding_ticker_1
from config_execution_api import price_rounding_ticker_2
from config_execution_api import quantity_rounding_ticker_1
from config_execution_api import quantity_rounding_ticker_2
from ..Strategy.func_cointegration import extract_close_prices
import math


# Get trade details and latest prices
def get_trade_details(orderbook, direction='long', capital=0):
    # Set calculation and output variables
    price_rounding = 0
    quantity_rounding = 0
    mid_price = 0
    quantity = 0
    stop_loss = 0
    bid_items_list = []
    ask_items_list = []

    # Get prices, stop loss and quantity
    if orderbook:

        # Set price rounding
        price_rounding = price_rounding_ticker_1 if orderbook[0]['symbol'] == ticker_1 else price_rounding_ticker_2
        quantity_rounding = quantity_rounding_ticker_1 if orderbook[0][
                                                              'symbol'] == ticker_1 else quantity_rounding_ticker_2

        # Organize prices
        for level in orderbook:
            if level['side'] == 'Buy':
                bid_items_list.append(level['price'])
            else:
                ask_items_list.append(level['price'])

        # Calculate the price, size, stop loss and average liquidity
        if len(ask_items_list) > 0 and len(bid_items_list) > 0:

            # Sort lists
            bid_items_list.sort(reverse=True)
            ask_items_list.sort()

            # Get nearest ask, bid and orderbook spread
            nearest_ask = ask_items_list[0]
            nearest_bid = bid_items_list[0]

            # Calculate hard stop loss
            if direction == 'long':
                mid_price = nearest_bid
            else:
                mid_price = nearest_ask

            stop_loss = round(mid_price * (1 + stop_loss_fail_safe), price_rounding)

    # Output results
    return mid_price, stop_loss, quantity
