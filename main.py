import asyncio
import logging


from datetime import datetime
from valr_python import WebSocketClient
from valr_python.enum import TradeEvent
from valr_python.enum import WebSocketType

from Keys import *
from Open_orders import *
from Trade_data import *

logging.basicConfig(filename='bot.log',
                    filemode='w',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
TRADE_EVENT = TradeEvent.NEW_TRADE_BUCKET
CURRENCY_PAIR = "BTCZAR"


def pretty_hook(data: dict):
    utc_now = datetime.utcnow()     # start time
    logging.info(f"{utc_now}, 1")   # log start time
    trade_data = TradeData(data)
    if trade_data.period60sec():
        open_orders()
        print(trade_data.low_tic)
    logging.info(f"{datetime.utcnow() - utc_now}, 4")  # end time


c = WebSocketClient(api_key=API_KEY, api_secret=API_SECRET, currency_pairs=[CURRENCY_PAIR],
                    ws_type=WebSocketType.TRADE.name,
                    trade_subscriptions=[TRADE_EVENT.name],
                    hooks={TRADE_EVENT.name: pretty_hook})

loop = asyncio.get_event_loop()

loop.run_until_complete(c.run())

# notes:
# 1) In log file if just start and end num given than most likely 300/900/1800/3600 bucket.
