import os
import tornado.httpserver
import tornado.ioloop
import tornado.web
from conf import conf
from web_handlers import *


class Application(tornado.web.Application):

    def __init__(self):
        handlers = [
            (r"/upload", UploadHandler),
        ]

        _settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "../www/templates"),
            static_path=os.path.join(os.path.dirname(__file__), "../www/static"),
            cookie_secret="..",
            login_url="auth/login",
            debug=True,
            serve_traceback=True,
            autoescape=True,
        )

        super(Application, self).__init__(handlers, **_settings)


def main():
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(conf.HTTP_PORT)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
