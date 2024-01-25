from config_execution_api import ws_public_url
from config_execution_api import ticker_1
from config_execution_api import ticker_2

from pybit.unified_trading import WebSocket
from time import sleep

# Web Socket Connection
ws = WebSocket(
    testnet=True,
    channel_type="linear",
)

global_orderbook = {}
global_trade = {}


def handle_message(message):
    global global_orderbook, global_trade

    topic = message.get('topic', '')
    if 'orderbook.50' in topic:
        global_orderbook = message
    elif 'publicTrade' in topic:
        global_trade = message


ws.orderbook_stream(50, f"{ticker_1}", handle_message)
ws.orderbook_stream(50, f"{ticker_2}", handle_message)
ws.trade_stream(f"{ticker_1}", handle_message)
ws.trade_stream(f"{ticker_2}", handle_message)

while True:
    sleep(1)
    if global_orderbook and global_trade:
        print("Orderbooks:", global_orderbook)
        print("Trades:", global_trade)
