class Conf(object):
    __slot__ = (
        'MYSQL_TABLE_PREFIX', HTTP_PORT
        )
    MYSQL_TABLE_PREFIX = 'web_analyse_'
    HTTP_PORT = 80