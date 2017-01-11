__all__ = ('cache_day_avg', 'check_key_exists')

from my_redis import MyRedis
from pymysql.err import ProgrammingError


def cache_day_avg(func):
    def warpper(user_id, time_stamp):
        return func(user_id, time_stamp)
    return warpper


def check_key_exists(func, *args, **kwargs):

    def _warpper():
        timestamp = kwargs.get('timestamp')
        table, date_str = self.gen_table(timestamp)
        if self.redis.get_failed_table(date_str):
            return False
        kwargs.insert(0, table)
        try:
            return func(*args, **kwargs)
        except ProgrammingError as e:
            self.redis.add_failed_table(date_str)
            self.logger.warn(e)
            return False

    return _warpper