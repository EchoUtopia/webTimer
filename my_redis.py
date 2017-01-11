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

    class MysqlTable(object):

        key = conf.REDIS_KEY.table_name
        expire = conf.REDIS_TABLE_EXPIRE

        @staticmethod
        def add(cls, redis_obj, date_str):
            cls.key = cls.key.format(date_str)
            redis_obj.redis.setex(cls.key, 1, cls.expire)

        @staticmethod
        def get(cls, redis_obj, date_str):
            cls.key = cls.key.format(date_str)
            redis_obj.redis.get(cls.key)

    class FailedMysqlTable(object):

        key = conf.REDIS_KEY.failed_table_name
        expire = conf.REDIS_TABLE_EXPIRE

        @staticmethod
        def add(cls, redis_obj, date_str):
            cls.key = cls.key.format(date_str)
            redis_obj.redis.setex(cls.key, 1, cls.expire)

        @staticmethod
        def get(cls, redis_obj, date_str):
            cls.key = cls.key.format(date_str)
            redis_obj.redis.get(cls.key)

    class LastMysqlTable(object):

        key = conf.REDIS_KEY.last_table

        @staticmethod
        def set(cls, redis_obj, date_str):
            cls.key = cls.key.format(date_str)
            redis_obj.redis.set(cls.key, 1)

        @staticmethod
        def get(cls, redis_obj, date_str):
            cls.key = cls.key.format(date_str)
            redis_obj.redis.get(cls.key)





