import pymysql
import time
from common import Singleton
from my_logger import MyLogger
from conf import conf


class MySQLConnection(Singleton):

    def __init__(self):
        self.conn   = None
        self.logger = MyLogger()
        self._conn()

    def _conn(self):
        try:
            self.conn = pymysql.connect(** conf.DB_CONFIG)
            return True
        except Exception as e:
            self.logger.error(e)
            return False

    def reconn(self, number=10, stime=1):
        _number = 0
        _status = False

        while not _status:
            try:
                self.conn.ping()
                _status = True
                return _status
            except :
                _number += 1
                time.sleep(stime)
                if _number == number:
                    raise


    def get_cursor(self):
        return self.conn.cursor()

    def close_conn(self):
        self.conn.close()