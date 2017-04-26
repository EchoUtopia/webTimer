import pymysql
import time
import Queue
from common import Singleton
from my_logger import MyLogger
from conf import conf
from pymysql.err import Error

class MySQLConnection(Singleton):

    def __init__(self):
        self.logger = MyLogger()
        self._conn()
        self.pool = Queue.Queue(maxsize=conf.MAX_POOL_SIZE)
        self._init_pool()

    def _init_pool(self):
        for _ in range(0, conf.MAX_POOL_SIZE):
            self.pool.put(self._conn())

    def get_connection(self):
        conn = self.pool.get()
        self._maybe_reconn(conn)
        return conn

    def return_connection(self, conn):
        # conn.commit()
        return self.pool.put(conn)

    def _conn(self):
        try:
            conn = pymysql.connect(** conf.DB_CONFIG)
            conn.autocommit(True)
            return conn
        except Exception as e:
            self.logger.error(e)
            return False

    def _maybe_reconn(self, conn):
        try:
            conn.ping(reconnect=True)
        except Error as e:
            self.logger.warn(e)
            raise e

    def close_conn(self):
        while not self.pool.empty():
            self.pool.get().close()