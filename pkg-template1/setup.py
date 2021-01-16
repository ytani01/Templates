#
# (c) 2021 Yoichi Tanibayashi
#
"""
setup.py for Python 3
"""
__author__ = 'Yoichi Tanibayashi'
__copyright__ = 'Copyright 2021, Yoichi Tanibayashi'
__credits__ = ['Yoichi Tanibayashi']

__version__ = '0.0.1'
__date__ = '2021/01'
__email__ = 'yoichi@tanibayashi.jp'

import os
from setuptools import setup, find_packages

_PKG_NAME = 'mypkg'
_URL = 'https://github.com/ytani01/Templates/'


def read_requirements():
    """Parse requirements from requirements.txt."""
    reqs_path = os.path.join('.', 'requirements.txt')
    with open(reqs_path, 'r') as f:
        requirements = [line.rstrip() for line in f]
    return requirements


with open("README.md") as f:
    long_description =f.read()

setup(
    name=_PKG_NAME,
    version=__version__,
    description='My package',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=__author__,
    author_email=__email__,
    url=_URL,
    license='MIT',
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
    ],
    install_requires=read_requirements(),
    packages=find_packages(exclude=('tests', 'docs')),
    python_requires='>=3.7',
)
