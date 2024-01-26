from config_execution_api import session
from config_execution_api import limit_order_basis
from func_calculations import get_trade_details
from config_execution_api import ticker_1
from config_execution_api import ticker_2


# Set Leverage
def set_leverage(ticker):
    leverage = session.set_leverage(
        category="linear",
        symbol=ticker,
        buyLeverage="1",
        sellLeverage="1",
    )

    # Return
    return


# Place limit or market order
def place_order(ticker, price, quantity, direction, stop_loss):
    side = 'Buy ' if direction == 'long' else 'Sell'

    # Place limit order
    if limit_order_basis:
        order = session.place_order(
            category="linear",
            symbol=ticker,
            side=side,
            orderType="Limit",
            qty=quantity,
            price=price,
            timeInForce="PostOnly",
            stopLoss=stop_loss,
        )
    else:
        order = session.place_order(
            category="linear",
            symbol=ticker,
            side=side,
            orderType="Market",
            qty=quantity,
            timeInForce="GoodTillCancel",
            stopLoss=stop_loss,
        )

    # Return
    return order


# Initialise execution
def initialise_order_execution(orderbook, ticker, direction, capital):
    if orderbook:
        mid_price, stop_loss, quantity = get_trade_details(orderbook, direction, capital)
        print(mid_price, stop_loss, quantity)

        if quantity > 0:
            order = place_order(ticker, mid_price, quantity, direction, stop_loss)
            print(order)

            if 'result' in order.keys():
                if 'orderId' in order['result']:
                    return order['result']['orderId']

    # Return
    return 0


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
# ws.orderbook_stream(50, f"{ticker_2}", handle_message)
#
# while True:
#     if global_orderbook:
#         initialise_order_execution(global_orderbook, ticker_2, 'short', 1000)
#         break


