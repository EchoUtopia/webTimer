import time
from aop import *
from my_logger import MyLogger
from my_redis import MyRedis
from MySQLConnection import MySQLConnection
from conf import conf
from common import *
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor


@singleton
class MySQLQuery:

    def __init__(self):
        self.connection = MySQLConnection()
        self.cursor = self.connection.get_cursor()
        self.logger = MyLogger().logger
        self.redis = MyRedis()
        self.executor = ThreadPoolExecutor(conf.THREAD_NUM)

    @staticmethod
    def gen_table(timestamp, _type="day"):

        timestamp = timestamp or time.localtime()
        _format = ""
        if _type == "day":
            _format = "%Y%m%d"
        elif _type == "month":
            _format = "%Y%m"
        elif _type == "year":
            _format = "%Y"
        date_str = time.strftime(_format, timestamp)
        #TODO to cache the date_str for performance
        return "%s%s" % (conf.MYSQL_TABLE_PREFIX, date_str), date_str

    @run_on_executor
    def create_table(self, timestamp):

        table_name, _ = self.gen_table(timestamp)
        sql = '''
        CREATE TABLE `%s` (
          `user_id` bigint not null,
          `ip` bigint(32) NOT NULL,
          `domain` varchar(100) NOT NULL,
          `time` bigint(24) not null,
          `total_time` smallint NOT NULL,
          PRIMARY KEY (`user_id`),
          KEY `analyse_user` (`user_id`)
        ) ENGINE=MyISAM DEFAULT CHARSET=utf8
        ''' % table_name
        try:
            self.cursor.execute(sql)
            self.cursor.commit()
            return table_name
        except Exception as e:
            self.logger.error("create table error: %s" % e)
            # if self.connection.reconn():
            #     # self.create_table()
            #
            # else:
            #     self.logger.error("reconnection mysql failed")

    @run_on_executor
    def insert_table(self, timestamp, user_id, ip, total_time, domain):

        table, date_str = self.gen_table(timestamp)
        sql = '''
            insert into %s ('user_id','ip','time','total_time', 'domain') values(%s,%s,%s,%s,%s)
        '''
        try:
            self.cursor.execute(sql, (table, user_id, ip, time, total_time, domain))
            self.cursor.commit()
            self.redis.add_mysql_table(date_str)
        except Exception as e:
            self.logger.error(e)
            return False

        else:
            return True

    @run_on_executor
    def select(self, timestamp, sql, params):
            self.cursor.execute(sql, params)
            return self.cursor.fetchmany()

    @run_on_executor
    def day_avg_time(self, user_id, time_stamp=None):
        #TODO find table name in redis, if not found return false
        sql = '''
            select avg(total_time) from %s where user_id = %s
        '''
        self.cursor.execute(sql, (self.gen_table(time_stamp), user_id))
        return self.cursor.fetchone()


