import logging

from sqlite3_functions import create_connection, add_period60sec
from datetime import datetime


class TradeData:
    def __init__(self, data: dict):
        self.data = data

    def period60sec(self):
        """Add 60 sec data for VALR to sqlite3 DB and create variables
        :return: True (working) or False(error)
        """
        if self.data['data']['bucketPeriodInSeconds'] == 60:
            self.data = self.data['data']
            conn = create_connection("TradeDataBTCZAR.db")
            add_period60sec(conn, self.data)
            logging.info(f"{datetime.utcnow()}, 2")  # The websockets one min bucket.
            self.start_time = self.data['startTime']
            self.close_tic = int(self.data['close']) - 300000  # todo fix
            self.open_tic = self.data['open']
            self.high_tic = self.data['high']
            self.low_tic = int(self.data['low']) - 300000  # todo fix
            self.quoteVolume_tic = ['quoteVolume']
            self.volume_tic = self.data['volume']
            return True
        else:
            return False
