__author__ = 'Jochem Berends <jberends+xppkg@jbits.nl>'
__home_page__ = 'https://github.com/jberends/xppkg'

# This version is used by the setup.py
__version__ = '0.2dev.0'

import sys

def main():
    """
    This is the main start point (entry point) of the script
    """
    sys.stdout.write("""
    Thanks for using XPpkg, the X-Plane hassle free package manager.

    Please remember that this is only version: %s.
    So go check out %s
    on which contributions are always welcome!

    Regards,
    %s
    """ % (__version__, __home_page__, __author__))
    pass




if __name__ == "__main__":
    exit = main()
    if exit:
        sys.exit(exit)
