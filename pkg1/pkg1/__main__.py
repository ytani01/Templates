#
# (c) 2021 Yoichi Tanibayashi
#
"""
"""
import click
from . import func1


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(invoke_without_command=True,
             context_settings=CONTEXT_SETTINGS,
             help="""
pkg1 command
""")
@click.pass_context
def cli(ctx):
    """ command group """
    subcmd = ctx.invoked_subcommand

    if not subcmd:
        print(ctx.get_help())


@cli.command(help="""
cmd1
""")
@click.argument('arg1', type=str)
def cmd1(arg1):
    """ cmd1 """
    func1(arg1)


if __name__ == '__main__':
    cli(prog_name='pkg1')
