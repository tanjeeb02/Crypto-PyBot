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


def handle_message(message):
    print(message)


ws.orderbook_stream(50, f"{ticker_1}", handle_message)
ws.orderbook_stream(50, f"{ticker_2}", handle_message)

while True:
    sleep(1)

