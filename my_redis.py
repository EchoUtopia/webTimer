import redis
from common import singleton

@singleton
class MyRedis:
    def __init__(self,host="127.0.0.1",port=6379,db=0):
        self.pool = redis.ConnectionPool(host=host,port=port,db=db)
        self.redis = redis.Redis(connection_pool=pool)

    def get_table(self,user,ip,timestamp=None,_type="day"):

        timestamp = timestamp or time.localtime()
        if _type == "day":
            _format = "%Y%m%d"
        elif _type == "month":
            _format = "%Y%m"
        elif _type == "year":
            _format = "%Y"
        date_str = time.strftime(_format, timestamp)
        return "%s:%s:%s" % (date_str,user,ip)

    def get_mysql_table():
        pass
