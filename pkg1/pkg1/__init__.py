#
# Copyright (c) 2021 Yoichi Tanibayashi
#
__prog_name__ = 'pkg1'
__version__ = '0.0.4'
__author__ = 'Yoichi Tanibayashi'

from .cmd2 import cmd2
from .mod1 import func1
from .my_logger import get_logger

all = ['cmd2',
       'func1',
       'get_logger', __prog_name__, __version__, __author__]
