#!/usr/bin/env python
# coding: utf-8

"""Usage: colordesk [options] FILE

Process FILE to show its color patterns in a web page.

Arguments:
  FILE        a yaml file that contains color pattern definitions.

Options:
  -h --help
  -p PORT --port=PORT   port for web server to listen [default: 8888]
  -d --debug            enter debug mode
"""

import os
import logging
from docopt import docopt
from tornado import httpserver, ioloop
from tornado.web import RequestHandler, Application
from tornado.log import enable_pretty_logging
from tornado.options import options


root_path = os.path.dirname(__file__)


class IndexHandler(RequestHandler):
    def get(self):
        self.render('index.html')


def run():
    args = docopt(__doc__)
    # print args

    # Set logging level
    options.logging = 'INFO'
    if args['--debug']:
        options.logging = 'DEBUG'
    enable_pretty_logging(options)

    application = Application(
        [
            (r'/', IndexHandler),
        ],
        static_path=os.path.join(root_path, 'static'),
        template_path=os.path.join(root_path, 'template'),
        debug=args['--debug'],
    )
    for host, rules in application.handlers:
        for i in rules:
            logging.debug('URL rule %s', i.regex.pattern)

    http_server = httpserver.HTTPServer(application)
    http_server.listen(args['--port'])
    if args['--debug']:
        print 'Enter debug mode'
    print 'Colordesk server started: http://127.0.0.1:%s' % args['--port']
    try:
        ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        print 'Stop colordesk server.'
