__all__ = ('cache_day_avg',)

from my_redis import MyRedis

def cache_day_avg(func)
    def warpper(user_id, time_stamp):
        return func(user_id, timestamp)
    return warpper