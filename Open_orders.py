import logging

from valr_python import Client
from datetime import datetime
from sqlite3_functions import clear_table, add_all_open_orders, create_connection, \
    get_open_orders_info, update_process_position_buy_price
from Keys import *


def open_buy_orders(orders):  # todo add sqlite table for buy orders
    """
    :param orders:
    :return:
    """
    placed_buys = []
    for order in orders:
        if order["currencyPair"] == "BTCZAR":
            if order["side"] == "buy":
                try:
                    placed_buys.append(int(order["price"]))
                except KeyError:
                    pass
    return placed_buys


def open_sell_orders(all_open_trades):  # todo add sqlite table for buy orders
    """
    :param all_open_trades:
    :return:
    """
    placed_sells = []
    for order in all_open_trades:
        if order["currencyPair"] == "BTCZAR":
            if order["side"] == "sell":
                try:
                    placed_sells.append(int(order["price"]))
                except KeyError:
                    pass
    return placed_sells


def buy_orders_to_place(buys_to_place, buys_placed):
    return list(set(buys_to_place) - set(buys_placed))


def buy_orders_to_cancel(buys_to_place, buys_placed):
    return list(set(buys_placed) - set(buys_to_place))


def all_open_orders(api_key: str = API_KEY, api_secret: str = API_SECRET, currency_pair: str = "BTCZAR"):
    btc_orders = []
    u = Client(api_key=api_key, api_secret=api_secret)
    open_trades = u.get_all_open_orders()
    for trade in open_trades:
        if trade["currencyPair"] == currency_pair:
            btc_orders.append(trade)
    return btc_orders


def add_btc_orders(conn, orders):
    for order in orders:
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


'''
def open_orders():
    """create a instance of OpenOrders and save data to sqlite3 table
    :return:
    """
    i = OpenOrders(api_key=API_KEY, api_secret=API_SECRET)
    return i.get_all_open_orders()


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
        btc_orders = []
        logging.info(f"{datetime.utcnow()}, 3")  # The get orders API call
        conn = create_connection("TradeDataBTCZAR.db")
        clear_table(conn, "all_open_orders")  # clear table for all_open_orders
        for order in all_orders:
            if order["currencyPair"] == "BTCZAR":
                btc_orders.append(order)
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
        return btc_orders
'''
