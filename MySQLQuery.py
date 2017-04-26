import time
from aop import *
from my_logger import MyLogger
from MySQLConnection import MySQLConnection
from conf import conf
from common import *
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor


class MySQLQuery(Singleton):

    def __init__(self, redis):
        self.connection = MySQLConnection()
        self.logger = MyLogger().logger
        self.redis = redis
        self.executor = ThreadPoolExecutor(conf.THREAD_NUM)

    @staticmethod
    def gen_table(timestamp, _type="month"):

        timestamp = timestamp and time.localtime(float(timestamp)) or time.localtime()
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

    @get_and_return_connection
    def create_table(self, table_name, **_):

        sql = '''
        CREATE TABLE if not exists `%s` (
          `id` bigint not null auto_increment,
          `user_id` bigint not null,
          `ip` varchar(100) NOT NULL,
          `domain` varchar(100) NOT NULL,
          `timestamp` bigint(24) not null,
          `total_time` smallint NOT NULL,
          PRIMARY KEY (`id`)
        ) ENGINE=MyISAM DEFAULT CHARSET=utf8
        ''' % table_name
        try:
            cursor = _['connection'].cursor()
            cursor.execute(sql)
            cursor.close()
            return table_name
        except Exception as e:
            self.logger.error("create table error: %s" % e)
            # print sql
            raise
            # if self.connection.reconn():
            #     # self.create_table()
            #
            # else:
            #     self.logger.error("reconnection mysql failed")
    @add_executor_param
    @run_on_executor
    @get_and_return_connection
    def insert_table(self, timestamp, user_id, ip, domains, **_):
        db_conn = _.get('connection')
        if db_conn is None:
            return
        table, date_str = self.gen_table(timestamp)
        if not self.redis.get_last_table(date_str):
            print "creating table"
            table = self.create_table(table)
            if table:
                self.redis.set_last_table(date_str)

        sql = "insert into %s (user_id,ip,timestamp,total_time,domain) values(%s,%s,%s,%s,%s);" % \
              (table, '%s', '%s', '%s', '%s', '%s')
        print sql
        try:
            cursor = db_conn.cursor()
            args = [(user_id, ip, timestamp, total_time, domain) for domain, total_time in domains.iteritems()]
            cursor.executemany(sql, args)

            # self.redis.add_mysql_table(date_str)
            cursor.close()
        except Exception as e:
            self.logger.error(e)
            raise

        else:
            return True

    @run_on_executor
    @check_key_exists
    @get_and_return_connection
    def select(self, timestamp, sql, params, **_):
        cursor = _['connection'].cursor()
        cursor.execute(sql, params)
        cursor.close()
        return self.cursor.fetchmany()

    @run_on_executor
    @check_key_exists
    @get_and_return_connection
    def day_avg_time(self, user_id, timestamp=None, **_):
        #TODO find table name in redis, if not found return false
        sql = '''
            select avg(total_time) from %s where user_id = %s
        '''
        cursor = _['connection'].cursor()
        cursor.execute(sql, (_['table'], user_id))
        cursor.close()
        return self.cursor.fetchone()

    def __getattr__(self, item):
        return self.connection.__getattribute__(item)