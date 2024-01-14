from config_execution_api import signal_positive_ticker
from config_execution_api import signal_negative_ticker


# Get positions
def get_position_info(ticker):

    # Declare variables
    side = 0
    size = ''

    # Get position info
    position = session_private.my_position(symbol=ticker)
    if 'ret_msg' in position.keys():
        if position['ret_msg'] == 'OK':
            if len(position['result']) == 2:
                if position['result'][0]['size'] > 0:
                    size = position['result'][0]['size']
                    side = 'Buy'
                else:
                    size = position['result'][1]['size']
                    side = 'Sell'

    # Return output
    return size, side
