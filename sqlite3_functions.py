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


def get_all_buys_to_place(conn, low_tic):
    """Get a list of all the buy order that need/have been placed
    :param conn: the Connection object
    :param low_tic: the low from the one minute candle
    :return: a list of all the buy orders that should be placed
    """
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM trades_bot WHERE {low_tic} < buyPrice < {low_tic * 1.05}")
    return cur.fetchall()
