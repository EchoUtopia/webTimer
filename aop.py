__all__ = ('cache_day_avg', 'check_key_exists', 'add_executor_param', \
           'get_and_close_connection')

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


def add_executor_param(func, *args, **kwargs):

    def _warpper():
        kwargs['executor'] = self.executor
        func(*args, **kwargs)
    return _warpper

def get_and_close_connection(func, *args, **kwargs):

    def _warpper():
        print args,kwargs
        kwargs['connection'] = self.connection.get_connection()
        try:
            func(self, *args, **kwargs)
        except Exception as e:
            raise e
        finally:
            self.return_connection(kwargs['connection'])
    return _warpper