#
# (c) 2020 Yoichi Tanibayashi
#
"""
my_logger.py
"""
__author__ = 'Yoichi Tanibayashi'
__date__ = '2021'

from logging import getLogger, StreamHandler, Formatter
from logging import DEBUG, INFO
# from logging import NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL

FMT_HDR = '%(asctime)s %(levelname)s '
FMT_LOC = '%(filename)s.%(name)s.%(funcName)s:%(lineno)d> '
HANDLER_FMT = Formatter(FMT_HDR + FMT_LOC + '%(message)s',
                        datefmt='%H:%M:%S')

CONSOLE_HANDLER = StreamHandler()
CONSOLE_HANDLER.setFormatter(HANDLER_FMT)


def get_logger(name, dbg=False):
    """
    get logger
    """
    logger = getLogger(name)

    # [Important !! ]
    # isinstance()では、boolもintと判定されるので、
    # 先に bool かどうかを判定する

    if isinstance(dbg, bool):
        if dbg:
            CONSOLE_HANDLER.setLevel(DEBUG)
            logger.setLevel(DEBUG)
        else:
            CONSOLE_HANDLER.setLevel(INFO)
            logger.setLevel(INFO)

    elif isinstance(dbg, int):
        CONSOLE_HANDLER.setLevel(dbg)
        logger.setLevel(dbg)

    else:
        raise ValueError('invalid `dbg` value: %s' % (dbg))

    logger.propagate = False
    logger.addHandler(CONSOLE_HANDLER)

    return logger
