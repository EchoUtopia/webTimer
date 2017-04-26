from common import *


class Conf(Singleton):
    __slot__ = (
        'MYSQL_TABLE_PREFIX', 'HTTP_PORT', 'DB_CONFIG', 'THREAD_NUM'
        'LOG_DIR', 'LOG_PATH', 'REDIS_TABLE_EXPIRE', 'REDIS_KEY',
        'REDIS_PERSIST', 'REDIS_CACHE','MAX_POOL_SIZE', 'CALL_LIMIT',
        )

    LOG_DIR = "."
    LOG_PATH = "web_analysis.log"
    MYSQL_TABLE_PREFIX = 'web_analyse_'
    HTTP_PORT = 8888
    DB_CONFIG   =   {
        'host'  :'localhost',
        'user'  :'root',
        'password'  :'root',
        'db'    :'web_analysis',
        'port'  :3306,
        'charset'   :"utf8"
    }
    THREAD_NUM = 5
    MAX_POOL_SIZE = 5
    REDIS_TABLE_EXPIRE = 3600
    REDIS_KEY = DotDict({
        "all_tables"    :"all_tables",
        "failed_table_name" :"failed_table:{0}",
        "last_table"    :"last_table:{0}",
        "last_upload_time": "last_upload_time",
    })
    REDIS_PERSIST = {
        "host"  :"localhost",
        "port"  :"63380",
        "db"    :0
    }
    REDIS_CACHE = {
        "host"  :"localhost",
        "port"  :"6379",
        "db"    :0
    }

    CALL_LIMIT = {#seconds
        'upload_interval': 150,
    }

conf = Conf()
