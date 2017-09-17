import docopt
from xppkg import __version__

__author__ = 'jochem'

__doc__ = """
XPpkg - the hassle free X-Plane package installer

Usage:
    xppkg install (<package-name>|<url>) [-v]
    xppkg check <file> [-v]
    xppkg uninstall <package-name> [-v]

Options:
    -h --help       Display help information
    -v --verbose    More information
    --version       Display version
"""

if __name__ == '__main__':
    arguments = docopt.docopt(__doc__, help=__doc__, version=__version__)
    from pprint import pprint

    pprint(arguments)
