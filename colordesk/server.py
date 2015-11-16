#!/usr/bin/env python
# coding: utf-8

import os
import logging
from tornado import httpserver, ioloop
from tornado.web import RequestHandler, Application
from tornado.log import enable_pretty_logging
from tornado.options import options

from .core import parse_patterns_yaml


root_path = os.path.dirname(__file__)


class IndexHandler(RequestHandler):
    @property
    def yaml_file(self):
        return self.application.yaml_file

    def get(self):
        patterns = parse_patterns_yaml(self.yaml_file)
        logging.debug('patterns: %s', patterns)
        self.render('index.html', patterns=patterns)


def run(filename, port=None, debug=False):
    # print args

    # Set logging level
    options.logging = 'INFO'
    if debug:
        print 'Enter debug mode'
        options.logging = 'DEBUG'
    enable_pretty_logging(options)

    application = Application(
        [
            (r'/', IndexHandler),
        ],
        static_path=os.path.join(root_path, 'static'),
        template_path=os.path.join(root_path, 'template'),
        debug=debug,
    )
    for host, rules in application.handlers:
        for i in rules:
            logging.debug('URL rule %s', i.regex.pattern)

    application.yaml_file = filename

    http_server = httpserver.HTTPServer(application)
    http_server.listen(port)
    print 'Colordesk server started: http://127.0.0.1:%s' % port

    try:
        ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        print 'Stop colordesk server.'
