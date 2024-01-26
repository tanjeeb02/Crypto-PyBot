from config_execution_api import stop_loss_fail_safe
from config_execution_api import ticker_1
from config_execution_api import ticker_2
from config_execution_api import price_rounding_ticker_1
from config_execution_api import price_rounding_ticker_2
from config_execution_api import quantity_rounding_ticker_1
from config_execution_api import quantity_rounding_ticker_2
import math
from decimal import Decimal, ROUND_HALF_UP


# Put close prices into a list
def extract_close_prices(prices):
    close_prices = []
    if 'result' in prices and 'list' in prices['result']:
        for item in prices['result']['list']:
            if math.isnan(float(item[4])):
                return []
            else:
                close_prices.append(float(item[4]))
    return close_prices


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
        price_rounding = price_rounding_ticker_1 if orderbook['data']['s'] == ticker_1 else price_rounding_ticker_2
        quantity_rounding = quantity_rounding_ticker_1 if orderbook['data'][
                                                              's'] == ticker_1 else quantity_rounding_ticker_2

        # Organize prices
        if len(orderbook['data']['b']) > 0:
            for i in range(0, len(orderbook['data']['b'])):
                bid_items_list.append(float(orderbook['data']['b'][i][0]))
        if len(orderbook['data']['a']) > 0:
            for i in range(0, len(orderbook['data']['a'])):
                ask_items_list.append(float(orderbook['data']['a'][i][0]))

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
                stop_loss = round(mid_price * (1 - stop_loss_fail_safe), price_rounding)
            else:
                mid_price = nearest_ask
                stop_loss = round(mid_price * (1 + stop_loss_fail_safe), price_rounding)

            # Calculate quantity
            quantity = round(capital / mid_price, quantity_rounding)

    # Output results
    return mid_price, stop_loss, quantity


# from pybit.unified_trading import WebSocket
#
# ws = WebSocket(
#     testnet=True,
#     channel_type="linear",
# )
#
# global_orderbook = {}
#
#
# def handle_message(message):
#     global global_orderbook
#
#     topic = message.get('topic', '')
#     if 'orderbook.50' in topic:
#         global_orderbook = message
#
#
# ws.orderbook_stream(50, f"{ticker_1}", handle_message)
#
# while True:
#     if global_orderbook:
#         mid_price_n, stop_loss_n, quantity_n = get_trade_details(global_orderbook, 'short', 1000)
#         print(mid_price_n, stop_loss_n, quantity_n)
