import time
import redis
from common import *
from conf import conf


class MyRedis(Singleton):
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

    def add_table(self, date_str):
        key = conf.REDIS_KEY.table_name.format(date_str)
        self.redis.setex(key, 1, conf.REDIS_TABLE_EXPIRE)

    def set_table(self, date_str):
        key = conf.REDIS_KEY.table_name.format(date_str)
        return self.redis.get(key)

    def add_failed_table(self, date_str):
        key = conf.REDIS_KEY.failed_table_name.format(date_str)
        self.redis.setex(key, 1, conf.REDIS_TABLE_EXPIRE)

    def set_failed_table(self, date_str):
        key = conf.REDIS_KEY.failed_table_name.format(date_str)
        return self.redis.get(key)

    def set_last_table(self, date_str):
        key = conf.REDIS_KEY.last_table.format(date_str)
        self.redis.set(key, 1)

    def get_last_table(self, date_str):
        key = conf.REDIS_KEY.last_table.format(date_str)
        return self.redis.get(key)







