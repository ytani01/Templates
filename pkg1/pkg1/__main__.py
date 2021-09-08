#
# Copyright (C) 2021 Yoichi Tanibayashi
#
"""
pkg1
"""
import click
from . import *
from . import __prog_name__, __version__, __author__


@click.group(invoke_without_command=True,
             context_settings=dict(help_option_names=['-h', '--help']),
             help=" by " + __author__)
@click.version_option(version=__version__)
@click.pass_context
def cli(ctx,):
    """ command group """
    subcmd = ctx.invoked_subcommand

    if not subcmd:
        print(ctx.get_help())


@cli.command(help=" by " + __author__)
@click.argument('arg1', type=str)
@click.option('--debug', '-d', 'debug', is_flag=True, default=False,
              help='debug flag')
def cmd1(arg1, debug):
    """ cmd1 """
    __log = get_logger(__name__, debug)
    __log.debug('name=%s', __name__)
    
    func1(arg1, debug)


if __name__ == '__main__':
    cli(prog_name=__prog_name__)
