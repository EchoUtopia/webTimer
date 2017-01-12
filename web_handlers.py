import json
import tornado.web
import tornado.gen
from MySQLQuery import MySQLQuery
from my_logger import MyLogger


class BaseHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.query = MySQLQuery()
        self.logger = MyLogger()
        self.ip = self.request.remote_ip

    def get_current_user(self):
        return {'user_id'   :1}


class HomeHandler(BaseHandler):
    pass


class RegisterHandler(BaseHandler):
    pass


class LoginHandler(BaseHandler):
    pass


class LogoutHandler(BaseHandler):
    pass


class UploadHandler(BaseHandler):

    @tornado.gen.coroutine
    def post(self):
        data = json.loads(self.request.body)
        domains = data.get('domains_data')
        timestamp = data.get('timestamp')
        user_id = self.get_current_user()['user_id']
        futures = []
        for domain, total_time in domains.iteritems():
            future = yield self.query.insert_table(timestamp, user_id, self.ip, total_time, domain)
            futures.append(future)
        for i in futures:
            print i
            if i.exception:
                self.logger.err(i.exception)


class DayHandler(BaseHandler):
    pass


class WeekHandler(BaseHandler):
    pass


class MonthHandler(BaseHandler):
    pass


class YearHandler(BaseHandler):
    pass
