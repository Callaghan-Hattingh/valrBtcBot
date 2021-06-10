import asyncio
import logging

from valr_python import WebSocketClient
from valr_python.enum import TradeEvent
from valr_python.enum import WebSocketType

from Keys import *
from bot_function import bot_market
from startup_check import start_up

from sqlite3_functions import *

logging.basicConfig(filename='tmp/logging_btczar_bot.log',
                    filemode='w',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
TRADE_EVENT = TradeEvent.NEW_TRADE_BUCKET
CURRENCY_PAIR = "BTCZAR"
CHECK_STARTUP = True

if CHECK_STARTUP:
    start_up()
    CHECK_STARTUP = False


def pretty_hook(data: dict):
    bot_market(data)


if __name__ == "__main__":
    c = WebSocketClient(api_key=API_KEY, api_secret=API_SECRET, currency_pairs=[CURRENCY_PAIR],
                        ws_type=WebSocketType.TRADE.name,
                        trade_subscriptions=[TRADE_EVENT.name],
                        hooks={TRADE_EVENT.name: pretty_hook})
    loop = asyncio.get_event_loop()

    while True:
        try:
            loop.run_until_complete(c.run())
        except asyncio.IncompleteReadError as e:
            logging.error(f"asyncio.IncompleteReadError: {e}")
            continue
        else:
            continue
            

# notes:
# 1) In log file if just start and end num given than most likely 300/900/1800/3600 bucket.
