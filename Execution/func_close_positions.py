from config_execution_api import signal_positive_ticker
from config_execution_api import signal_negative_ticker
from config_execution_api import session


# Get positions
def get_position_info(ticker):
    # Declare variables
    side = 0
    size = ''

    # Get position info
    position = session.get_positions(category="linear", symbol=ticker)
    if 'retMsg' in position.keys():
        if position['retMsg'] == 'OK':
            if position['result']['list'][0]['side'] == 'Buy':
                side = 'Buy'
                size = position['result']['list'][0]['size']
            else:
                side = 'Sell'
                size = position['result']['list'][0]['size']

    # Return output
    return side, size


# Place market close order
def place_market_close_order(ticker, side, size):
    # side = 'Sell' if side == 'Buy' else 'Buy'
    # Close position
    session.place_order(
        category="linear",
        symbol=ticker,
        side=side,
        orderType="Market",
        qty=size,
    )

    # Return
    return


# Close all positions for both tickers
def close_all_positions(kill_switch):
    # Cancel all active orders
    session.cancel_all_orders(category='linear', settleCoin='USDT')
    session.cancel_all_orders(category='linear', settleCoin='USDT')

    # Get position information
    side_1, size_1 = get_position_info(signal_positive_ticker)
    side_2, size_2 = get_position_info(signal_negative_ticker)

    if int(size_1) > 0:
        place_market_close_order(signal_positive_ticker, side_2, size_1)

    if int(size_2) > 0:
        place_market_close_order(signal_negative_ticker, side_1, size_2)

    # Return
    kill_switch = 0
    return kill_switch

