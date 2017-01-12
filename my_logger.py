import logging
import os
from common import Singleton
from conf import conf


class MyLogger(Singleton):

    def __init__(self, level=None):
        self.logger = logging.getLogger()
        _dir = conf.LOG_DIR
        _path = "%s/%s" % (_dir, conf.LOG_PATH)
        if not os.path.exists(_dir):
            os.mkdir(_dir)
        if not os.path.isfile(_path):
            f = open(_path, "w")
            f.close()
        self.handler = logging.FileHandler(_path)
        formatter = logging.Formatter('%(asctime)s   %(levelname)s   %(message)s')
        self.handler.setFormatter(formatter)
        self.logger.addHandler(self.handler)
        level = logging.__dict__.get(level, logging.DEBUG)
        self.logger.setLevel(level)

    def __getattr__(self, name):
        return self.logger.__getattribute__(name)