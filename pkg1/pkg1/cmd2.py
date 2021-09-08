#
# Copyright (c) 2021 Yoichi Tanibayashi
#
import click
from .my_logger import get_logger
from .mod1 import func1


@click.command(help="cmd2")
@click.argument('arg1', type=str)
@click.option('--debug', '-d', 'debug', is_flag=True, default=False,
              help='debug flag')
@click.pass_obj
def cmd2(obj, arg1, debug):
    """ cmd1 """
    __log = get_logger(__name__, obj['debug'] or debug)
    __log.debug('obj=%s, arg1=%s', obj, arg1)

    func1(arg1)
