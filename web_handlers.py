import json
import tornado.web
import tornado.gen
from my_redis import MyRedis
from MySQLQuery import MySQLQuery
from my_logger import MyLogger
from aop import *


class BaseHandler(tornado.web.RequestHandler):
    def initialize(self):
        redis = MyRedis()
        self.redis = redis
        self.query = MySQLQuery(redis=redis)
        self.logger = MyLogger()
        self.ip = self.request.remote_ip

    def get_current_user(self):
        user_cookie = self.get_secure_cookie("user")
        if user_cookie:
            user = json.loads(user_cookie)
            self.user_id = user['user_id']
            return user
        return None



class UploadHandler(BaseHandler):

    @tornado.gen.coroutine
    @upload_limit
    def post(self):
        data = json.loads(self.request.body)
        domains = data.get('domains_data')
        if domains is None or not isinstance(domains, dict) or len(domains) > 60:
            return
        keys = domains.iterkeys()
        for k in keys:
            if len(k) > 67:
                return
            if domains[k] == 0:
                domains.pop(k)
        timestamp = data.get('timestamp')
        user_id = self.current_user
        future = self.query.insert_table(timestamp, user_id, self.ip, domains)
        if future.exception():
            print future.exception()
            self.logger.error(future.exception())
        self.write({})
        return
