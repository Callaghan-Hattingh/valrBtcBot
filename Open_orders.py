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
    return i.get_all_open_orders()


def open_buy_orders(all_open_orders):  # todo add sqlite table for buy orders
    """
    :param all_open_orders:
    :return:
    """
    placed_buys = []
    for order in all_open_orders:
        if order["currencyPair"] == "BTCZAR":
            if order["side"] == "buy":
                try:
                    placed_buys.append(order["customerOrderId"])
                except KeyError:
                    pass
                # print(order)
    logging.info(f"{datetime.utcnow()}, 4")  # list of customerOrderId on the exchange
    # print(f"{placed_buys}\n")
    return placed_buys


def buy_orders_to_place(buys_to_place, buys_placed):
    return list(set(buys_to_place) - set(buys_placed))


def buy_orders_to_cancel(buys_to_place, buys_placed):
    return list(set(buys_placed) - set(buys_to_place))


class OpenOrders:  # todo rework function turn sqlite into a separate function
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
        conn = create_connection("TradeDataBTCZAR.db")
        clear_table(conn, "all_open_orders")  # clear table for all_open_orders
        for order in all_orders:
            if order["currencyPair"] == "BTCZAR":
                try:
                    add_all_open_orders(conn, order)
                except KeyError:
                    logging.info(f"{datetime.utcnow()}, OpenOrders - KeyError - Trade without customerOrderId")
                    pass  # Want to skip open orders without customerOrderId
                    # The get orders API call
                except Exception as e:
                    logging.error(f"Exception occurred: {e}", exc_info=True)
                else:
                    pass
        return all_orders

    def get_all_open_sell_orders(self):  # todo add sqlite table for sell orders
        all_orders = self.client.get_all_open_orders()
        conn = create_connection("TradeDataBTCZAR.db")
        for order in all_orders:
            try:
                add_all_open_orders(conn, order)
            except KeyError:
                order["customerOrderId"] = order["orderId"]
                add_all_open_orders(conn, order)
