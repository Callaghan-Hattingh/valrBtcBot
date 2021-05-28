import sqlite3
from sqlite3 import Error


def create_connection(db_file: str):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn


def clear_table(conn, table: str):
    """Clear the data in a sqlite table
    :param conn: the Connection object
    :param table: the table
    :return:
    """
    cur = conn.cursor()
    cur.execute(f"DELETE FROM {table};")
    conn.commit()


def add_period60sec(conn, data: dict):
    """Add the 60sec trade data to the sqlite3 database
    :param conn: the Connection object
    :param data: the trade data
    :return:
    """
    cur = conn.cursor()
    cur.execute("INSERT INTO period60sec VALUES (?,?,?,?,?,?,?,?,?)", [data["currencyPairSymbol"],
                                                                       data["bucketPeriodInSeconds"],
                                                                       data["startTime"],
                                                                       data["open"],
                                                                       data["high"],
                                                                       data["low"],
                                                                       data["close"],
                                                                       data["close"],
                                                                       data["quoteVolume"]])
    conn.commit()


def add_all_open_orders(conn, data: dict):
    """Add all the open orders trade data to the sqlite3 database
    :param conn: the Connection object
    :param data: the trade data
    :return:
    """
    cur = conn.cursor()
    cur.execute("INSERT INTO all_open_orders VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?);",
                [data["createdAt"],
                 data["currencyPair"],
                 data["customerOrderId"],
                 data["filledPercentage"],
                 data["orderId"],
                 data["originalQuantity"],
                 data["price"],
                 data["remainingQuantity"],
                 data["side"],
                 data["status"],
                 data["timeInForce"],
                 data["type"],
                 data["updatedAt"]])
    conn.commit()


def get_open_orders_info(conn, buy_price: int):
    """Get a list of all the buy order that need/have been placed
        :param conn: the Connection object
        :param buy_price: the low of the candle
        :return: a list of all the buy orders that should be placed
        """
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM all_open_orders WHERE price = '{buy_price}';")
    return cur.fetchall()


def get_all_buys_to_place(conn, high_price: int, low_price: int):
    """Get a list of all the buy order that need/have been placed
    :param conn: the Connection object
    :param low_price: the low of the candle - x amount
    :param high_price: the close of the candle
    :return: a list of all the buy orders that should be placed (buyPrice)
    """
    cur = conn.cursor()
    cur.execute(f"SELECT buyPrice FROM trades_bot WHERE buyPrice BETWEEN {low_price} AND {high_price}")
    items = cur.fetchall()
    return [i[0] for i in items]


def get_info_buy_price(conn, buy_price: int):
    """Get a list of all the buy order that need/have been placed
    :param conn: the Connection object
    :param buy_price: the low of the candle
    :return: a list of all the buy orders that should be placed
    """
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM trades_bot WHERE buyPrice = {buy_price};")
    return cur.fetchall()


def get_info_customer_order_id(conn, customer_order_id: str):
    """Get a list of all the buy order that need/have been placed
    :param conn: the Connection object
    :param customer_order_id: the low of the candle
    :return: a list of all the buy orders that should be placed
    """
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM trades_bot WHERE customerOrderId = '{customer_order_id}';")
    return cur.fetchall()


def update_process_position(conn, customer_order_id: str, process_position: int = 0):
    """UPDATE the process_position based on the customer_order_id
    :param conn: the Connection object
    :param customer_order_id: the low of the candle
    :param process_position:
                    0 - Wait to place buy
                    1 - Placed buy
                    2 - Part buy
                    3 - Bought
                    4 - To place sell
                    5 - Placed sell
                    6 - Part sell
                    7 - Sold
                    8 - Profit placement
                    9 - Reset
    :return:
    """
    cur = conn.cursor()
    cur.execute(f"""UPDATE trades_bot SET processPosition = {process_position} 
                    WHERE customerOrderId = '{customer_order_id}';""")
    conn.commit()


def update_process_position_buy_price(conn, buy_price: int, process_position: int = 0):
    """UPDATE the process_position based on the customer_order_id
    :param conn: the Connection object
    :param buy_price: the low of the candle
    :param process_position:
                    0 - Wait to place buy
                    1 - Placed buy
                    2 - Part buy
                    3 - Bought
                    4 - To place sell
                    5 - Placed sell
                    6 - Part sell
                    7 - Sold
                    8 - Profit placement
                    9 - Reset
    :return:
    """
    cur = conn.cursor()
    cur.execute(f"""UPDATE trades_bot SET processPosition = {process_position} 
                    WHERE buyPrice = '{buy_price}';""")
    conn.commit()
