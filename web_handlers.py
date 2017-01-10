import tornado.web
from MySQLQuery import MySQLQuery


class BaseHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.query = MySQLQuery()

class HomeHandler(BaseHandler):
    pass


class RegisterHandler(BaseHandler):
    pass


class LoginHandler(BaseHandler):
    pass


class LogoutHandler(BaseHandler):
    pass


class UploadHandler(BaseHandler):
    def post(self):
        pass


class DayHandler(BaseHandler):
    pass


class WeekHandler(BaseHandler):
    pass


class MonthHandler(BaseHandler):
    pass


class YearHandler(BaseHandler):
    pass
