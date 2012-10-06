__author__ = 'Jochem Berends <jberends+xppkg@jbits.nl>'
__home_page__ = 'https://github.com/jberends/xppkg'

QUESTIONNAIRE_URL = 'http://bit.ly/XPPKGQ1'

# This version is used by the setup.py
__version__ = '0.3dev.0'

import sys
import os, platform

def main():
    """
    This is the main start point (entry point) of the script
    """
    sys.stdout.write("""
    Thanks for using XPpkg, the X-Plane hassle free package manager.

    Please remember that this is only version: %s.
    So go check out %s
    on which contributions are always welcome!

    While the work is done on the functionality you will be directed
    to a small questionnaire... too understand what you want.

    Regards,
    %s
    """ % (__version__, __home_page__, __author__))
    try:
        launch_link(QUESTIONNAIRE_URL)
    except:
        pass #silently
    pass


def launch_link(url_to_open, do_raise=None):
    """
    Launches an URL link based on the platform
    """
    # source: http://www.dwheeler.com/essays/open-files-urls.html
    the_platform = platform.system()
    if the_platform == 'Win':
        command = 'cmd /c start %s' % url_to_open
    elif the_platform == 'Darwin':
        command = 'open %s' % url_to_open
    elif the_platform == 'Linux':
        command = 'xdg-open %s' % url_to_open
    else:
        command = 'None'

    if command:
        try:
            os.system(command)
        except:
            if do_raise:
                raise
            else:
                pass #silently


if __name__ == "__main__":
    exit = main()
    if exit:
        sys.exit(exit)
