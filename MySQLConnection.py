import MySQLdb
import time
from common import singleton

@singleton
class MySQLConnection:
    def __init__(self,host,user,password,db,port = 3306,charset=utf8):
        self.host   = host  
        self.user   = user  
        self.password = password  
        self.db     = db  
        self.port   = port  
        self.charset= charset  
        self.conn   = None  
        self._conn()  

    def conn(self):
        try:
            self.conn = MySQLdb.Connection(self.host,self.user,self.password,self.db,self.port,self.charset)
            return True
        except:
            return False

    def reconn(self,number=100,stime=1):
        _number = 0
        _status = False

        while not _status and _number < number:
            try:
                self.conn.ping()
                _status = True
            except:
                _number += 1
                time.sleep(stime)
        return _status
    def get_cursor(self):
        return self.conn.cursor

    def close_conn(self):
        self.conn.close()