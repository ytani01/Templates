#
# Copyright (c) 2021 Yoichi Tanibayashi
#
import click
from .my_logger import get_logger


class Cmd3:
    """ Cmd3 """

    __log = get_logger(__name__, False)

    def __init__(self, debug=False):
        self._dbg = debug
        __class__.__log = get_logger(__class__.__name__, self._dbg)

    def cmd3(self, arg1):
        """ method1 """
        self.__log.debug('arg=%s', arg1)

        print('Hello, %s' % (arg1))


@click.command(help="cmd3")
@click.argument('arg1', type=str)
@click.option('--debug', '-d', 'debug', is_flag=True, default=False,
              help='debug flag')
@click.pass_obj
def cmd3(obj, arg1, debug):
    """ cmd3 """
    debug = obj['debug'] or debug

    __log = get_logger(__name__, debug)
    __log.debug('obj=%s, arg1=%s', obj, arg1)

    cmd_obj = Cmd3(debug=debug)
    cmd_obj.cmd3(arg1)
