import logging
import os
from common import Singleton


class MyLogger(Singleton):

    def __init__(self, level=None):
        self.logger = logging.getLogger()
        _dir = "/var/log/web_analyse"
        _path = "%s/web_analyse" % _dir
        if os.path.exists(_dir):
            os.mkdir(_dir)
        if os.path.isfile(_path):
            f = open(_path, "w")
            f.close()
        self.handler = logging.FileHandler(_path)
        formatter = logging.Formatter('%(asctime)s   %(levelname)s   %(message)s')
        self.handler.setFormatter(formatter)
        self.logger.addHandler(self.handler)
        level = logging.__dict__.get(level, logging.DEBUG)
        self.logger.setLevel(level)

