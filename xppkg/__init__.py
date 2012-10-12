from backwardcompat import main_during_development
from util import launch_link
import sys

__author__ = 'Jochem Berends <jberends+xppkg@jbits.nl>'
__home_page__ = 'https://github.com/jberends/xppkg'

QUESTIONNAIRE_URL = 'http://bit.ly/XPPKGQ1'

# This version is used by the setup.py
__version__ = '0.3dev.2'


if __name__ == "__main__":
    exit = main_during_development()
    if exit:
        sys.exit(exit)
