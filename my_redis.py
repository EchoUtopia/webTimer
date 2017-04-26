import time
import redis
from common import *
from conf import conf


class MyRedis(Singleton):
    def __init__(self):
        self._pool = redis.ConnectionPool(**conf.REDIS_CACHE)
        self.redis = redis.Redis(connection_pool=self._pool)
        self._persist_pool = redis.ConnectionPool(**conf.REDIS_PERSIST)
        self.persist_redis = redis.Redis(connection_pool=self._persist_pool)

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
        key = conf.REDIS_KEY.all_tables
        self.persist_redis.sadd(key, date_str)

    def table_exists(self, table):
        key = conf.REDIS_KEY.all_tables
        member = table.replace(conf.MYSQL_TABLE_PREFIX,'')
        return self.persist_redis.sismember(key, member)

    def add_failed_table(self, date_str):
        key = conf.REDIS_KEY.failed_table_name.format(date_str)
        self.redis.setex(key, 1, conf.REDIS_TABLE_EXPIRE)

    def get_failed_table(self, date_str):
        key = conf.REDIS_KEY.failed_table_name.format(date_str)
        return self.redis.get(key)

    def set_last_table(self, date_str):
        key = conf.REDIS_KEY.last_table.format(date_str)
        self.redis.set(key, 1)

    def get_last_table(self, date_str):
        key = conf.REDIS_KEY.last_table.format(date_str)
        return self.redis.get(key)

    def get_last_upload_time(self, user_id):
        key = conf.CALL_LIMIT.upload_limit
        return self.redis.hget(key, user_id)







