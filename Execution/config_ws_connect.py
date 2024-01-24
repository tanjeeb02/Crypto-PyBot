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

global_orderbooks = {}
global_trades = {}


def handle_message(message):
    global global_orderbooks, global_trades

    topic = message.get('topic', '')
    if 'orderbook.50' in topic:
        global_orderbooks = message
    elif 'publicTrade' in topic:
        global_trades = message['data'][0]['S']


ws.orderbook_stream(50, f"{ticker_1}", handle_message)
ws.trade_stream(f"{ticker_1}", handle_message)

while True:
    sleep(1)
    print("Orderbooks:", global_orderbooks)
    print("Trades:", global_trades)
