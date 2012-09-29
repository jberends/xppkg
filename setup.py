#!/usr/bin/python
"""
XPpkg, the X-Plane package installer
"""

__author__ = 'Jochem Berends'
__author_email__ = 'jberends+xppkg@jbits.nl'

from xppkg import __version__
from distutils.core import setup

classifiers = """\
Development Status :: 2 - Pre-Alpha
Environment :: Console
Intended Audience :: Developers
Programming Language :: Python
Topic :: Games/Entertainment :: Simulation
"""


setup(
    name='XPpkg',
    author=__author__,
    author_email='%s <%s>' % (__author__, __author_email__),
    url='https://github.com/jberends/xppkg',
    version=__version__,
    description='X-Plane hassle free package installer',
    classifiers=classifiers.splitlines(),
    packages=['xppkg',],
    license='Attribution-NonCommercial-ShareAlike 3.0 (CC BY-NC-SA 3.0)',
    long_description=open('README.rst').read(),
)