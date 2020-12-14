#!/usr/bin/env python3
#
# (c) 2020 Yoichi Tanibayashi
#
"""
Python3 template

### for detail and simple usage ###

$ python3 pydoc TemplateA.ClassA


### sample program ###

$ ./TemplateA.py -h

"""
__author__ = 'Yoichi Tanibayashi'
__date__   = '2020'

from MyLogger import get_logger


class ClassA:
    """
    Description
    -----------

    Simple Usage
    ============
    ## Import

    from TemplateA import ClassA

    ## Initialize

    obj = ClassA()


    ## method1

    obj.method1(arg)


    ## End of program

    obj.end()

    ============

    Attributes
    ----------
    attr1: type(int|str|list of str ..)
        description
    """
    __log = get_logger(__name__, False)

    def __init__(self, opt, debug=False):
        """ Constructor

        Parameters
        ----------
        opt: type
            description
        """
        self._dbg = debug
        __class__.__log = get_logger(__class__.__name__, self._dbg)
        self.__log.debug('opt=%s', opt)

        self._opt = opt

    def end(self):
        """
        Call at the end of program
        """
        self.__log.debug('doing ..')
        print('end of %s' % __class__.__name__)
        self.__log.debug('done')

    def method1(self, arg):
        """
        Description

        Parameters
        ----------
        arg: str
            description
        """
        self.__log.debug('arg=%s', arg)

        print('%s:%s' % (arg, self._opt))

        self.__log.debug('done')


# --- 以下、サンプル ---


class SampleApp:
    """ Sample application class

    Attributes
    ----------
    """
    __log = get_logger(__name__, False)

    def __init__(self, arg, opt, debug=False):
        """constructor

        Parameters
        ----------
        arg: str
            description
        opt: str
            description
        """
        self._dbg = debug
        __class__.__log = get_logger(__class__.__name__, self._dbg)
        self.__log.debug('arg=%s, opt=%s', arg, opt)

        self._arg = arg
        self._opt = opt

        self._obj = ClassA(self._opt, debug=self._dbg)

    def main(self):
        """ main routine
        """
        self.__log.debug('')

        for a in self._arg:
            self._obj.method1(a)

        self.__log.debug('done')

    def end(self):
        """ Call at the end of program.
        """
        self.__log.debug('doing ..')
        self._obj.end()
        self.__log.debug('done')


import click
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(context_settings=CONTEXT_SETTINGS, help='''
ClassA sample program
''')
@click.argument('arg', type=str, nargs=-1)
@click.option('--opt', '-o', 'opt', type=str, default='def_value',
              help='sample option: default=%s' % 'def_value')
@click.option('--debug', '-d', 'debug', is_flag=True, default=False,
              help='debug flag')
def main(arg, opt, debug):
    """サンプル起動用メイン関数
    """
    __log = get_logger(__name__, debug)
    __log.debug('arg=%s, opt=%s', arg, opt)

    app = SampleApp(arg, opt, debug=debug)
    try:
        app.main()
    finally:
        __log.debug('finally')
        app.end()


if __name__ == '__main__':
    main()
