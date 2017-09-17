#!/usr/bin/python
"""
XPpkg, the X-Plane package installer
"""

__author__ = 'Jochem Berends'
__author_email__ = 'jberends+xppkg@jbits.nl'

from xppkg import __version__
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
import sys

classifiers = """\
Development Status :: 2 - Pre-Alpha
Environment :: Console
Intended Audience :: Developers
Programming Language :: Python
Topic :: Games/Entertainment :: Simulation
"""

tests_require = ['nose',]

setup(
    name='XPpkg',
    author=__author__,
    author_email='%s <%s>' % (__author__, __author_email__),
    url='https://github.com/jberends/xppkg',
    version=__version__,
    description='X-Plane hassle free package installer',
    keywords='X-Plane package installer hassle-free',
    classifiers=classifiers.splitlines(),
    packages=['xppkg',],

    # These are the console scripts which are generated 'xppkg' and 'xppkg-<pyversion>'
    # They will be in your /Scripts directory (win) or bin dir (macosx, linux)
    entry_points={
        'console_scripts':[
            'xppkg=xppkg:main',
            'xppkg-%s=xppkg:main' % sys.version[:3]
            ],
        },

    license='Attribution-NonCommercial-ShareAlike 3.0 (CC BY-NC-SA 3.0)',
    long_description=open('README.rst').read(),

    test_suite='nose.collector',
    install_requires=[
        'requests',
    ],
    tests_require=tests_require,
    extras_require = {
        'testing':tests_require,
        },
)
