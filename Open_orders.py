import logging

from valr_python import Client
from datetime import datetime
from sqlite3_functions import clear_table, add_all_open_orders, create_connection
from Keys import *


def open_orders():
    """create a instance of OpenOrders and save data to sqlite3 table
    :return:
    """
    i = OpenOrders(api_key=API_KEY, api_secret=API_SECRET)
    i.get_all_open_orders()


class OpenOrders:
    """
    GET - ALL OPEN ORDERS
    process the open orders
    """
    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.client = Client(self.api_key, self.api_secret)

    def get_all_open_orders(self):
        all_orders = self.client.get_all_open_orders()
        logging.info(f"{datetime.utcnow()}, 3")  # The get orders API call
        conn = create_connection("TradeDataBTCZARbot.db")
        clear_table(conn, "all_open_orders")  # clear table for all_open_orders
        for order in all_orders:
            if order["currencyPair"] == "BTCZAR":
                try:
                    add_all_open_orders(conn, order)
                except KeyError:
                    logging.info(f"{datetime.utcnow()}, OpenOrders - KeyError - Trade without customerOrderId")
                    # The get orders API call
                    try:  # KeyError if there is no customer order ID
                        order["customerOrderId"] = order["orderId"]
                        add_all_open_orders(conn, order)
                    except Exception as e:
                        logging.error(f"Exception occurred: {e}", exc_info=True)
                    else:
                        pass
                    pass

    def get_all_open_buy_orders(self):  # todo add sqlite table for buy orders
        all_orders = self.client.get_all_open_orders()
        conn = create_connection("TradeDataBTCZARbot.db")
        for order in all_orders:
            if order["side"] == "buy":
                try:
                    add_all_open_orders(conn, order)
                except KeyError:
                    order["customerOrderId"] = order["orderId"]
                    add_all_open_orders(conn, order)

    def get_all_open_sell_orders(self):  # todo add sqlite table for sell orders
        all_orders = self.client.get_all_open_orders()
        conn = create_connection("TradeDataBTCZARbot.db")
        for order in all_orders:
            try:
                add_all_open_orders(conn, order)
            except KeyError:
                order["customerOrderId"] = order["orderId"]
                add_all_open_orders(conn, order)
