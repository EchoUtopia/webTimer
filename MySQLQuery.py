import time
from aop import *
from my_logger import MyLogger
from my_redis import MyRedis
from MysQLConnection import MysQLConnection

class MySQLQuery:

    def __init__(self,cursor):
        self.connection = MysQLConnection()
        self.cusror = self.connection.get_cursor()
        self.logger = Mylogger().logger
        self.redis = MyRedis()

    def get_table(self,timestamp,_type = "day"):

        timestamp = timestamp or time.localtime()
        if _type == "day":
            _format = "%Y%m%d"
        elif _type == "month":
            _format = "%Y%m"
        elif _type == "year":
            _format = "%Y"
        date_str = time.strftime(_format, timestamp)
        return "%s%s" % (settings.MYSQL_TABLE_PREFIX, date_str)


    def create_table(self,timestamp):

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
        ''' % self.get_table(timestamp)
        try:
            self.cursor.execute(sql)
            self.cursor.commit()
        except Exception, e:
            self.logger.error("create table error")
            if self.connection.reconn():
                self.create_table()
            else:
                self.logger.error("reconnection mysql failed")



    def insert_table(self, timestamp, user_id, ip, time, total_time, domain):

        table = self.get_table(timestamp)
        sql = '''
            insert into %s ('user_id','ip','time','total_time', 'domain') values(%s,%s,%s,%s,%s)
        '''
        self.cursor.execute(sql,(table,user_id,ip,time,total_time,domain))
        self.cursor.commit()


    def select(self, timestamp, sql, params):
        table = self.get_table(timestamp)
        params = params.insert(0,table)
        self.cursor.execute(sql,params)
        return self.cursor.fetchmany()

    def day_avg_time(self, user_id, time_stamp=None):
        #TODO find table name in redis, if not found return false
        sql = '''
            select avg(total_time) from %s where user_id = %s
        '''
        self.cursor.execute(sql,(self.get_table(timestamp),user_id))
        return self.cursor.fetchone()


