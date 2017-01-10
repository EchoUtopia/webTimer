from common import *


@singleton
class Conf(object):
    __slot__ = (
        'MYSQL_TABLE_PREFIX', 'HTTP_PORT', 'DB_CONFIG', 'THREAD_POOL'
        )
    MYSQL_TABLE_PREFIX = 'web_analyse_'
    HTTP_PORT = 8080
    DB_CONFIG   =   {
        'host'  :'localhost',
        'user'  :'appfame',
        'password'  :'three.appfame',
        'db'    :'web_analysis',
        'port'  :3306,
        'charset'   :"utf8"
    }
    THREAD_POOL = 5
    REDIS_TABLE_EXPIRE = 3600
    REDIS_KEY = {
        "table_name"    :"table:all",
        "failed_table_name" :"failed_table:all"
    }
    REDIS_PERSIST = {
        "host"  :"localhost",
        "port"  :"63380",
        "db"    :0
    }
    REDIS_CACHE = {
        "host"  :"localhost",
        "port"  :"63379",
        "db"    :0
    }

conf = Conf()
