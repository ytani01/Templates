#
# (c) 2021 Yoichi Tanibayashi
#
"""
mypkg
"""
__author__ = 'Yoichi Tanibayashi'
__version__ = '0.0.1'

__prog_name__ = 'Pkg2'

from .mod1 import MyClass1
from .webapp import WebServer
from .handler1 import Handler1
from .wshandler1 import WsHandler1

__all__ = [
    '__author__', '__version__', '__prog_name__',
    'MyClass1',
    'WebServer', 'Handler1', 'WsHandler1'
]
