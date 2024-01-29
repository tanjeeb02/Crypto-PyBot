from config_execution_api import session
from func_close_positions import get_position_info


# Check for open positions
def open_position_confirmation(ticker):
    try:
        position = session.get_positions(category="linear", symbol=ticker)
        if position['result']['list'][0]['size'] > 0:
            return True
    except:
        return True
    return False


# Check for active positions
def active_position_confirmation(ticker):
    try:
        active_order = session.get_open_orders(category='linear', symbol=ticker)

        if active_order['retMsg'] == 'OK':
            if active_order['result']['list'] is not None:
                return True
    except:
        return True


# Get active position price and quantity
def get_active_positions(ticker):
    # Get position
    active_order = session.get_open_orders(category='linear', symbol=ticker)

    order_status = ''
    side = ''
    size = 0
    price = 0

    # Get position info
    if 'retMsg' in active_order.keys():
        if active_order['retMsg'] == 'OK':
            order_status = active_order['result']['list'][0]['orderStatus']
            side = active_order['result']['list'][0]['side']
            size = active_order['result']['list'][0]['qty']
            price = active_order['result']['list'][0]['price']
        else:
            return '', '', 0, 0

    # Return output
    return order_status, side, size, price
