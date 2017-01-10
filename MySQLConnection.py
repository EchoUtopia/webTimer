import pymysql
import time
from common import singleton
from my_logger import MyLogger
from conf import conf


@singleton
class MySQLConnection:

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

        while not _status and _number < number:
            try:
                self.conn.ping()
                _status = True
            except :
                _number += 1
                time.sleep(stime)
        return _status

    def get_cursor(self):
        return self.conn.cursor

    def close_conn(self):
        self.conn.close()