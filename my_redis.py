import time
import redis
from common import *
from conf import conf


@singleton
class MyRedis:
    def __init__(self):
        self.pool = redis.ConnectionPool(**conf.REDIS_CACHE)
        self.redis = redis.Redis(connection_pool=self.pool)

    @staticmethod
    def get_key(user, ip, timestamp=None, _type="day"):

        timestamp = timestamp or time.localtime()
        if _type == "day":
            _format = "%Y%m%d"
        elif _type == "month":
            _format = "%Y%m"
        elif _type == "year":
            _format = "%Y"
        else:
            return False
        date_str = time.strftime(_format, timestamp)
        return "%s:%s:%s" % (date_str, user, ip)

    def add_mysql_table(self, date_str):
        key = conf.REDIS_KEY.key
        self.redis.sadd(key, date_str)

    def add_failed_table(self, date_str):
        key = conf.REDIS_KEY.failed_key
        self.redis.sadd(key, date_str)
        self.redis.expire(key, conf.REDIS_TABLE_EXPIRE)

    def get_failed_table(self, date_str):
        key = conf.REDIS_KEY.failed_key
        return self.redis.sismember(key, date_str)

    def get_mysql_table(self,):
        key = conf.REDIS_KEY.key
        return self.redis.lrange(key, 0, -1)



