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

from docopt import docopt
from .server import run


def main():
    args = docopt(__doc__)
    run(args['FILE'], debug=args['--debug'], port=args['--port'])
