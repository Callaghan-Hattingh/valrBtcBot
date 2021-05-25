import logging

from valr_python import Client
from Keys import *


c = Client(api_key=API_KEY, api_secret=API_SECRET)
limit_order = {
    "side": "BUY",
    "quantity": '0.001',
    "price": '10000',
    "pair": "BTCZAR",
    "post_only": True,
    "customer_order_id": "12345"
}
res = c.post_limit_order(**limit_order)
print(res)
