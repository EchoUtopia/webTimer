import tornado.web
from web_handler import *
import tornado.ioloop
import tornado.httpserver
class Application(tornado.web.Application):

    def __init__(self):
        handlers = [
            (r"/", HomeHandler),
            (r"/auth/register", RegisterHandler),
            (r"/auth/login", LoginHandler),
            (r"/auth/logout", LogoutHandler),
            (r"/upload", UploadHandler),
            (r"/day", DayHandler),
            (r"/week", WeekHandler),
            (r"/month", MonthHandler),
            (r"/year", YearHandler),
        ]

        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "../www/templates"),
            static_path=os.path.join(os.path.dirname(__file__), "../www/static"),
            cookie_secret = "..",
            login_url = "auth/login",
            debug = True,
            serve_traceback = True,
            autoescape = True,

        )

        super(Application, self).__init__(handlers, **settings)


def main():
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(settings.HTTP_PORT)
    tornado.ioloop.IOLoop.current().start()


if __name__ = "__main__":
    main()