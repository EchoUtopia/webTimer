import MySQLdb
import redis
import time

r = redis.Redis(host='localhost',port=6379,db=0)

def get_list():
    # return r.keys("*")
    return filter(lambda x:r.type(x) == "hash" and x.startswith("ip"),r.keys("*"))

def minute_to_timestamp(minute):
    minute = str(minute*5)
    strtime = time.strftime("%Y-%m-%d %H",time.localtime(time.time()))
    strtime = "%s:00" % strtime
    print strtime
    strptime = time.strptime("")