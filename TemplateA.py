#!/usr/bin/env python3
#
# (c) 2019 Yoichi Tanibayashi
#
import time

import click
from logging import getLogger, StreamHandler, Formatter, DEBUG, INFO, WARN
logger = getLogger(__name__)
logger.setLevel(INFO)
console_handler = StreamHandler()
console_handler.setLevel(DEBUG)
handler_fmt = Formatter(
    '%(asctime)s %(levelname)s %(name)s.%(funcName)s> %(message)s',
    datefmt='%H:%M:%S')
console_handler.setFormatter(handler_fmt)
logger.addHandler(console_handler)
logger.propagate = False
def get_logger(name, debug):
    l = logger.getChild(name)
    if debug:
        l.setLevel(DEBUG)
    else:
        l.setLevel(INFO)
    return l

#####
CONST='abc'

#####
class A:
    def __init__(self, word='', debug=False):
        self.debug = debug
        self.logger = get_logger(__class__.__name__, debug)
        self.logger.debug('word=%s', word)

        self.word = word

    def output(self):
        for w in self.word:
            print(w)
            print(w[::-1])

    def end(self):
        self.logger.debug('')
        
#####
class Sample:
    def __init__(self, word, debug=False):
        self.debug = debug
        self.logger = get_logger(__class__.__name__, debug)
        self.logger.debug('word=%s',word)

        self.obj = A(word, debug=debug)

    def main(self):
        self.logger.debug('')

        self.obj.output()

    def end(self):
        self.logger.debug('')
        self.obj.end()
        
#####
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument('word', type=str, nargs=-1)
@click.option('--debug', '-d', 'debug', is_flag=True, default=False,
              help='debug flag')
def main(word, debug):
    logger = get_logger('', debug)
    logger.debug('word=%s', word)

    obj = Sample(word, debug=debug)
    try:
        obj.main()
    finally:
        print('finally')
        obj.end()

if __name__ == '__main__':
    main()
