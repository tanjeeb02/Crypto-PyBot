"""
    API Documentation
    https://bybit-exchange.github.io/docs/v5/intro
"""

# API Imports
from pybit.unified_trading import HTTP
# from pybit.unified_trading import WebSocket

# CONFIG
kline_limit = 200
timeframe = 'D'
z_score_window = 20
mode = 'test'

# LIVE API
api_key_mainnet = ''
api_secret_mainnet = ''

# TEST API
api_key_testnet = 'odg1BU6zom7FjeK9aN'
api_secret_testnet = 'xaGNbnSlb2BfIz08vxZQzkjfhWICuVMpEbEb'

# SELECTED API
api_key = api_key_testnet if mode == 'test' else api_key_mainnet
api_secret = api_secret_testnet if mode == 'test' else api_secret_mainnet

# SESSION Activation
session = HTTP(
    testnet=True,
    api_key=api_key_testnet,
    api_secret=api_secret_testnet,
)

# # Web Socket Connection
# subs = [
#     'kline.30.BTCUSDT',
# ]
# ws = WebSocket(
#     'wss://stream.bybit.com/v5/public/linear',
#     subscriptions=subs,
# )
#
# while True:
#     data = ws.fetch(subs[0])
#     if data:
#         print(data)

