#!/usr/local/bin/python3
# coding:utf-8
"""Main Module."""

from tornado import httpserver, ioloop, web

from config import CFG as O_O
from routes import ROUTES as routes


def main():
    """Entrance Function"""

    tornado_app = web.Application(handlers=routes, **O_O.application)
    tornado_server = httpserver.HTTPServer(tornado_app, **O_O.httpserver)

    tornado_server.listen(O_O.server.port)
    print('start listen...')
    O_O.show()

    ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
