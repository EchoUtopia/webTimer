import time
from my_logger import MyLogger
from MysQLConnection import MysQLConnection

class MySQLQuery:

    def __init__(self,cursor):
        self.connection = MysQLConnection()
        self.cusror = self.connection.get_cursor()
        self.logger = Mylogger().logger

    def get_table(self,timestamp,_type = "day"):

        timestamp = timestamp or time.localtime()
        if _type == "day":
            _format = "%Y%m%d"
        elif _type == "month":
            _format = "%Y%m"
        elif _type == "year":
            _format = "%Y"
        date_str = time.strftime(_format, timestamp)
        return "web_analyse_%s" % date_str


    def create_table(self,timestamp):

        sql = '''
        CREATE TABLE `%s` (
          `user_id` bigint not null,
          `ip` bigint(32) NOT NULL,
          `time` bigint(24) not null,
          `total_time` smallint NOT NULL,
          `visit_count` int(11) NOT NULL,
          PRIMARY KEY (`time,user_id`),
          KEY `analyse_user` (`user_id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8
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



    def insert_db(self,timestamp,user_id,ip,time,total_time,visit_count):

        table = self.get_table(timestamp)
        sql = '''
            insert into %s ('user_id','ip','time','total_time','visit_count') values(%s,%s,%s,%s,%s)
        '''
        self.cursor.execute(sql,(table,user_id,ip,time,total_time,visit_count))
        self.cursor.commit()

    def select(self,timestamp,sql,params):
        table = self.get_table(timestamp)
        params = params.insert(0,table)
        result = self.cursor.execute(sql,params)
        return self.cursor.fetchmany(result)


