"""
    interval: 60, D
    from: integer from timestamp in seconds
    limit: max size of 200
"""

from config_strategy_api import session
from config_strategy_api import timeframe
from config_strategy_api import kline_limit
import datetime
import time

# Get start times
time_start_date = 0
if timeframe == 60:
    time_start_date = datetime.datetime.now() - datetime.timedelta(hours=kline_limit)
if timeframe == 'D':
    time_start_date = datetime.datetime.now() - datetime.timedelta(days=kline_limit)
time_start_seconds = int(time_start_date.timestamp())


# Get historical prices (klines)
def get_price_klines(symbol):
    # Get prices
    prices = session.get_mark_price_kline(
        category='linear',
        symbol=symbol,
        interval=timeframe,
        start=time_start_seconds,
        limit=kline_limit,
    )

    # Manage API calls
    # time.sleep(0.1)

    # Return output
    if len(prices['result']['list']) != kline_limit:
        return []
    else:
        return prices
