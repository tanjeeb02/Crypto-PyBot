from config_execution_api import ticker_1
from config_execution_api import ticker_2
from config_execution_api import session
from config_execution_api import timeframe
from config_execution_api import kline_limit
from func_calculations import extract_close_prices
import datetime
import time


# Get trade sizes
def get_ticker_trade_sizes(ticker):
    # Get trades history
    trades = session.get_public_trade_history(
        category='linear',
        symbol=ticker,
        limit=50,
    )

    # Get the list for calculating the avg order size
    quantity = []
    if 'result' in trades.keys():
        for trade in trades['result']['list']:
            quantity.append(float(trade['size']))

    # Return output
    if len(quantity) > 0:
        avg_order = sum(quantity) / len(quantity)
        res_trades_price = float(trades['result']['list'][0]['price'])

        return avg_order, res_trades_price

    return 0, 0


# Get start times
def get_timestamps():
    time_start_date = 0
    time_next_date = 0
    now = datetime.datetime.now()

    if timeframe == 60:
        time_start_date = now - datetime.timedelta(hours=kline_limit)
        time_next_date = now + datetime.timedelta(seconds=30)
    elif timeframe == 'D':
        time_start_date = now - datetime.timedelta(days=kline_limit)
        time_next_date = now + datetime.timedelta(minutes=1)

    time_start_seconds = int(time_start_date.timestamp())
    time_now_seconds = int(now.timestamp())
    time_next_seconds = int(time_next_date.timestamp())

    return time_start_seconds, time_now_seconds, time_next_seconds


# Get historical prices (klines)
def get_price_klines(ticker):
    # Get prices
    time_start_seconds, _, _ = get_timestamps()
    prices = session.get_mark_price_kline(
        category='linear',
        symbol=ticker,
        interval=timeframe,
        start=time_start_seconds,
        limit=kline_limit,
    )

    # Manage API calls
    time.sleep(0.1)

    # Return prices output
    return [] if len(prices['result']['list']) != kline_limit else prices


# Get latest klines
def get_latest_klines():
    series_1 = []
    series_2 = []
    prices_1 = get_price_klines(ticker_1)
    prices_2 = get_price_klines(ticker_2)

    if len(prices_1) > 0:
        series_1 = extract_close_prices(prices_1)
    if len(prices_2) > 0:
        series_2 = extract_close_prices(prices_2)

    return series_1, series_2
