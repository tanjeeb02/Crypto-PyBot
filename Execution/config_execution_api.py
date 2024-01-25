"""
    API Documentation
    https://bybit-exchange.github.io/docs/v5/intro
"""

# API Imports
from pybit.unified_trading import HTTP

# from pybit.unified_trading import WebSocket


# CONFIG
mode = 'test'
ticker_1 = 'ENSUSDT'
ticker_2 = 'LRCUSDT'
signal_positive_ticker = ticker_2
signal_negative_ticker = ticker_1
price_rounding_ticker_1 = 3
price_rounding_ticker_2 = 4
quantity_rounding_ticker_1 = 1
quantity_rounding_ticker_2 = 1

limit_order_basis = True

tradeable_capital_usdt = 2000  # to be split among the two tickers
stop_loss_fail_safe = 0.15  # 15% stop loss
signal_trigger_thresh = 1.1  # z-score threshold for trade signal

kline_limit = 200
timeframe = 'D'
z_score_window = 20

# LIVE API
api_key_mainnet = ''
api_secret_mainnet = ''

# TEST API
api_key_testnet = 'odg1BU6zom7FjeK9aN'
api_secret_testnet = 'xaGNbnSlb2BfIz08vxZQzkjfhWICuVMpEbEb'

# SELECTED API
api_key = api_key_testnet if mode == 'test' else api_key_mainnet
api_secret = api_secret_testnet if mode == 'test' else api_secret_mainnet

# URLs
ws_private_url = 'wss://stream-testnet.bybit.com/v5/private'
ws_public_url = 'wss://stream-testnet.bybit.com/v5/public/inverse'

# SESSION Activation
session = HTTP(
    testnet=True,
    api_key=api_key,
    api_secret=api_secret,
)


