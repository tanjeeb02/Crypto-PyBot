from func_close_positions import get_position_info
from func_position_calls import get_active_positions
from func_calculations import get_trade_details
from config_execution_api import ticker_1
from config_execution_api import ticker_2


# Check order items
def check_order(orderbook, ticker, order_id, remaining_capital, direction='Long'):
    # Get important parameters
    _, _, order_status = get_active_positions(ticker)
    _, quantity, price = get_position_info(ticker)

    # Determine action - trade complete - stop placing orders
    if quantity >= remaining_capital and quantity > 0:
        print(f'Quantity {quantity}', f'Remaining Capital {remaining_capital}')
        return 'Trade Complete'

    # Determine action - position filled - buy more
    if order_status == "Filled":
        return "Position Filled"

    # Determine action - order active - do nothing
    active_items = ["Created", "New"]
    if order_status in active_items:
        return "Order Active"

    # Determine action - partial filled order - do nothing
    if order_status == "PartiallyFilled":
        return "Partial Fill"

    # Determine action - order failed - try place order again
    cancel_items = ["Cancelled", "Rejected", "PendingCancel"]
    if order_status in cancel_items:
        return "Try Again"


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
#         check_order(global_orderbook, ticker_1, '', 0, 'Long')
