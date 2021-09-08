#
# Copyright (C) 2021 Yoichi Tanibayashi
#
from . import get_logger


def func1(arg='world', debug=False):
    __log = get_logger(__name__, debug)
    __log.debug('arg=%s', arg)

    print('Hello, %s' % (arg))
