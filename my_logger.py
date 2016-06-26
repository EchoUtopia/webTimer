import logging
import os
from common import singleton

@singleton
class MyLogger:

    def __init__(self,level):
        self.logger = loggin.getLogger()
        _dir = "/var/log/web_analyse"
        _path = "%s/web_analyse" % _dir
        if os.path.exists(_dir):
            os.mkdir(_dir)
        if os.isfile(_path):
            f = open(_path,"w")
            f.close()
        self.handler = logging.FileHandler(_path)
        formatter = logging.Formatter('%(asctime)s   %(levelname)s   %(message)s')
        self.handler.setFormatter(formatter)
        self.logger.addHandler(self.handler)
        level = logging.__dict__.get(level,loggin.DEBUG)
        self.logger.setLevel(level)

