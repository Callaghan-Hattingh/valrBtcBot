import logging

import simplejson
from valr_python import Client
from Keys import *


def post_limit_order(side: str, quantity: float, price: int, customer_order_id: str,
                     pair: str = "BTCZAR", post_only: bool = True):
    logging.info(f"{customer_order_id}, {side}: post_limit_order ")
    c = Client(api_key=API_KEY, api_secret=API_SECRET)
    limit_order = {
        "side": side,
        "quantity": f"{quantity}",
        "price": f"{price}",
        "pair": pair,
        "post_only": post_only,
        "customer_order_id": customer_order_id
    }
    return c.post_limit_order(**limit_order)


def delete_order(customer_order_id: str, pair: str = "BTCZAR"):
    c = Client(api_key=API_KEY, api_secret=API_SECRET)
    limit_order = {
        "pair": pair,
        "customer_order_id": customer_order_id
    }
    try:
        c.delete_order(**limit_order)
    except simplejson.errors.JSONDecodeError:
        pass
