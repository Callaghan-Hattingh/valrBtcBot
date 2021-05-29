import logging
from datetime import datetime

from Open_orders import open_buy_orders, buy_orders_to_place, buy_orders_to_cancel, \
    open_sell_orders, all_open_orders, add_btc_orders

from Trade_data import TradeData
from sqlite3_functions import *
from Post_orders import delete_order, post_limit_order


def bot_market(data: dict):
    """The main  function that brings all the other functions together to create a trading bot.
    :param data: the candles from the VALR websockets.
    :return:
    """
    utc_now = datetime.utcnow()  # start time
    logging.info(f"{utc_now}, 1")  # log start time
    trade_data = TradeData(data)
    if trade_data.period60sec():
        conn = create_connection("TradeDataBTCZAR.db")

        all_orders = all_open_orders()
        print(all_orders)
        add_btc_orders(conn, all_orders)

        if check_bought(conn, all_orders=all_orders):
            print("Buy has taken place.")

        if check_sold(conn, all_orders=all_orders):
            print("Sell has taken place.")

        buys_placed = open_buy_orders(all_orders)
        buys_to_place = get_all_buys_to_place(conn, trade_data.close_tic, trade_data.low_tic * 0.95)

        buy = buy_orders_to_place(buys_to_place, buys_placed)
        cancel = buy_orders_to_cancel(conn, buys_to_place, buys_placed)
        logging.info(f"Before buy/cancel buy, 5")

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
        print('\n')
    logging.info(f"{datetime.utcnow() - utc_now}, 6")  # end time


def check_bought(conn, all_orders):
    pp = get_process_position(conn, process_position=1)  # History
    i = [p[0] for p in pp]
    buys_placed = open_buy_orders(all_orders)  # present
    y = list(set(i) - set(buys_placed))
    print(y)
    return y


def check_sold(conn, all_orders):
    pp = get_process_position(conn, process_position=5)  # History
    i = [p[0] for p in pp]
    buys_placed = open_sell_orders(all_orders)  # present
    y = list(set(i) - set(buys_placed))
    print(y)
    return y


def check_part_buy(conn, all_orders):
    part_buy = []
    for i in all_orders:  # check for no partially filled orders
        u = float(get_open_orders_info(conn, i)[0][3])
        if u > 0:
            update_process_position_buy_price(conn, buy_price=i, process_position=2)
            part_buy.append(i)
    return part_buy


def check_part_sell():
    pass


def type_of_trade(orders, side: str):
    y = [i for i in orders if i["side"] == side]
    trades = []
    for order in orders:
        if order["side"] == side:
            trades.append(order)
    return trades
