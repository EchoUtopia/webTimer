__all__ = ('cache_day_avg', 'check_key_exists', 'add_executor_param', \
           'get_and_return_connection', 'upload_limit')

import functools
import time
from my_redis import MyRedis
from pymysql.err import ProgrammingError
from conf import conf


def cache_day_avg(func):
    def warpper(user_id, time_stamp):
        return func(user_id, time_stamp)
    return warpper


def check_key_exists(func, *args, **kwargs):

    def _warpper(func, self, *args, **kwargs):
        timestamp = kwargs.get('timestamp')
        table, date_str = self.gen_table(timestamp)
        if self.redis.get_failed_table(date_str):
            return False
        kwargs['table'] = table
        try:
            return func(*args, **kwargs)
        except ProgrammingError as e:
            self.redis.add_failed_table(date_str)
            self.logger.warn(e)
            return False

    return _warpper


def get_and_return_connection(func):

    def _warpper(self, *args, **kwargs):
        kwargs['connection'] = self.connection.get_connection()
        try:
            return func(self, *args, **kwargs)
        except Exception as e:
            print e
            raise e
        finally:
            self.return_connection(kwargs['connection'])
    return _warpper


def add_executor_param(func):
    def _warpper(self, *args, **kwargs):
        kwargs['executor'] = self.executor
        return func(self, *args, **kwargs)
    return _warpper


def upload_limit(func):

    def _wrapper(self):
        user_id = self.user_id
        last_upload_time = self.redis.get_last_upload_time(user_id)
        now = int(time.time())
        interval = conf.CALL_LIMIT.upload_interval
        if last_upload_time is None or now - int(last_upload_time) > interval:
            return func(self)

    return _wrapper



