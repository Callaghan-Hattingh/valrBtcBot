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
        conn = create_connection("TradeDataBTCZAR.db")
        all_orders = open_orders()
        buys_placed = open_buy_orders(all_orders)
        buys_to_place = get_all_buys_to_place(conn, trade_data.close_tic, trade_data.low_tic*0.95)
        # print(buys_placed)
        # print(buys_to_place)
        buy = buy_orders_to_place(buys_to_place, buys_placed)
        cancel = buy_orders_to_cancel(conn, buys_to_place, buys_placed)
        logging.info(f"Before buy/cancel buy, 5")
        # print(cancel)
        # print(buy)
        for item in cancel:
            coi = get_info_buy_price(conn, buy_price=item)[0][3]
            delete_order(customer_order_id=coi)
            update_process_position(conn, customer_order_id=coi, process_position=0)
        for i in buy:
            y = get_info_buy_price(conn, buy_price=i)  # gets info from sql table
            if y[0][9] == 0:
                q = post_limit_order(side="BUY", quantity=y[0][4], price=y[0][0], customer_order_id=y[0][3])
                if q["id"]:
                    update_process_position(conn, customer_order_id=y[0][3], process_position=1)
                    # if return a id assume order placed correctly and check order on the next candle
                else:
                    logging.error(f"No order id received: Message: {q}")
            else:
                logging.error(f"process position is incorrect, should be 0 is {y[0][9]}")
            pass
        print("\n")
    logging.info(f"{datetime.utcnow() - utc_now}, 6")  # end time


def check_bought():
    pass


def check_buy_place():
    pass


def check_buy_cancel():
    pass

