import logging
from sqlite3_functions import create_connection, get_process_position, update_process_position
from Post_orders import post_limit_order, order_status, last_trade_exchange
from Open_orders import all_open_orders
from bot_function import type_of_trade


def start_up():
    conn = create_connection("TradeDataBTCZAR.db")
    # check for 3
    check_startup_bought(conn)
    # check for 6
    check_startup_sold(conn)
    # compare open orders to process position
    check_sell_orders(conn)
    conn.close()


def check_startup_bought(conn):
    items = get_process_position(conn, process_position=3)
    for item in items:
        print(item)
        res = order_status(item[3])
        if res["orderStatusType"] == "Filled":
            last_trade = last_trade_exchange()
            post_limit_order(side="SELL", quantity=item[4], price=(int(last_trade[0]["price"]) + 25000),
                             customer_order_id=item[3])
            logging.error(f"check_startup_bought post_limit_order buy placed {item[3]}")
            print(f"check_startup_bought post_limit_order buy placed {item[3]}")
            update_process_position(conn, customer_order_id=item[3], process_position=4)
        elif res["orderStatusType"] == "Cancelled":
            update_process_position(conn, customer_order_id=item[3])
        elif res["orderStatusType"] == "Placed":
            update_process_position(conn, customer_order_id=item[3], process_position=1)
        else:
            print("check_startup_bought error:", res)
            logging.error(f"check_startup_bought {res}")


def check_startup_sold(conn):
    items = get_process_position(conn, process_position=6)
    for item in items:
        print(item)
        res = order_status(item[3])
        if res["orderStatusType"] == "Filled":
            pass
        elif res["orderStatusType"] == "Placed":
            update_process_position(conn, customer_order_id=item[3], process_position=4)
        else:
            print("check_startup_bought error:", res)
            logging.error(f"check_startup_bought {res}")


def check_sell_orders(conn):
    sell = set(get_process_position(conn, process_position=4))
    part_sell = set(get_process_position(conn, process_position=5))
    all_orders = all_open_orders()
    cur_sell = set(p["customerOrderId"] for p in type_of_trade(all_orders, side='sell'))
    items = list(cur_sell - sell - part_sell)
    for item in items:
        update_process_position(conn, customer_order_id=item, process_position=4)
