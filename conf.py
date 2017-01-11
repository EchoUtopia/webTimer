from common import *


class Conf(Singleton):
    __slot__ = (
        'MYSQL_TABLE_PREFIX', 'HTTP_PORT', 'DB_CONFIG', 'THREAD_NUM'
        )

    MYSQL_TABLE_PREFIX = 'web_analyse_'
    HTTP_PORT = 8888
    DB_CONFIG   =   {
        'host'  :'localhost',
        'user'  :'root',
        'password'  :'root',
        'db'    :'web_analyse',
        'port'  :3306,
        'charset'   :"utf8"
    }
    THREAD_NUM = 5
    REDIS_TABLE_EXPIRE = 3600
    REDIS_KEY = DotDict({
        "table_name"    :"table:%s",
        "failed_table_name" :"failed_table:%s",
        "last_table"    :"last_table:%s",
    })
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
