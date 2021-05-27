import logging
from datetime import datetime

from Open_orders import open_orders, open_buy_orders, buy_orders_to_place, buy_orders_to_cancel
from Trade_data import TradeData
from sqlite3_functions import *
from Post_orders import delete_order, post_limit_order


def bot_market(data: dict):
    """The main  function that brings all the other functions together to create a trading bot.
    :param data: the candles from the VALR websockets.
    :return:
    """
    utc_now = datetime.utcnow()     # start time
    logging.info(f"{utc_now}, 1")   # log start time
    trade_data = TradeData(data)
    if trade_data.period60sec():
        all_orders = open_orders()
        buys_placed = open_buy_orders(all_orders)
        conn = create_connection("TradeDataBTCZAR.db")
        buys_to_place = get_all_buys_to_place(conn, trade_data.close_tic, trade_data.low_tic*0.98)
        buy = buy_orders_to_place(buys_to_place, buys_placed)
        can = buy_orders_to_cancel(buys_to_place, buys_placed)
        logging.info(f"Before buy/cancel buy, 5")
        print(buy)
        for i in can:
            delete_order(customer_order_id=i)
        for i in buy:
            y = get_buy_place_info(conn, customer_order_id=i)  # gets info from sql table
            if y[0][9] == 0:
                q = post_limit_order(side="BUY", quantity=y[0][4], price=y[0][0], customer_order_id=i)
                if q["id"]:
                    update_process_position(conn, customer_order_id=i, process_position=1)
                    # if return a id assume order placed correctly and check order on the next candle
                else:
                    logging.error(f"No order id received: Message: {q}")
            else:
                logging.error(f"process position is incorrect, should be 0 is {y[0][9]}")
            pass
        print("\n")
    logging.info(f"{datetime.utcnow() - utc_now}, 6")  # end time
