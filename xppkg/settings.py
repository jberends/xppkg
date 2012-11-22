"""
Settings file for XPPKG

It includes logic to finds the X-SYSTEM location depending on your environment, bootstraps the settings
"""

import platform
import os
import urllib
import urlparse
import util
from xppkg.exceptions import SimulatorNotInstalledError

# For debugging purposes in testing phase


DEBUG = True

XSYSTEM_LOCATION_HELPERS={
    'Darwin':'/Applications/X-Plane 10/',
    'Windows':'C:/Program Files/X-Plane 10/',
    'Linux':'/opt/X-plane 10'
}

XPLANE_EXECUTABLE={
    'Darwin': 'X-Plane.app/Contents/MacOS/X-Plane',
    'Windows':'X-plane.exe',
    'Linux':'X-plane'
}

INSTALLATION_LOG='/Output/preferences/directory.txt'

SYSTEM = platform.system()
XSYSTEM_PATH = ''
XSYSTEM_VERSION = ''

XPPKG_INF_FILENAME = 'XPPKG-INF.yaml'
XPPKG_REPOS_URL = 'https://raw.github.com/jberends/xppkg/master/packages/'

# Ignored file patterns in the snap
SNAP_IGNORED_PATTERNS = ['.DS_Store','*.svn*', '*.git*', '*.png','*.gif' ]
if DEBUG:
    SNAP_IGNORED_PATTERNS.extend(['*.dsf','*.osf','*.osm','*.acf','*.wav','*.afl','*.txt','*.pdf',
                                  '*.obj','*.ter','*.pol','*.for','*.dds','*.wpn','*.bmp'])

"""
Bootstraps by discovering the XSYSTEM_PATH and XSYSTEM_VERSION
"""
def discover_XPlane():
    # set XSYSTEM_PATH this is a happy path, no searching
    global XSYSTEM_PATH, XSYSTEM_VERSION
    if os.path.exists(XSYSTEM_LOCATION_HELPERS[SYSTEM]) and\
       os.path.isfile(os.path.join(XSYSTEM_LOCATION_HELPERS[SYSTEM],
           XPLANE_EXECUTABLE[SYSTEM])):
        XSYSTEM_PATH = os.path.dirname(XSYSTEM_LOCATION_HELPERS[SYSTEM])
    else:
        raise SimulatorNotInstalledError,\
        ('Cannot find X-Plane installation at %s' % XSYSTEM_LOCATION_HELPERS[SYSTEM])
    # set XSYSTEM_VERSION
    get_version_cmd = [os.path.join(XSYSTEM_PATH, XPLANE_EXECUTABLE[SYSTEM]), '--version']
    XSYSTEM_VERSION = util.call_subprocess(get_version_cmd, show_stdout=False)

XPPKG_CATEGORIES_URL = urlparse.urljoin(XPPKG_REPOS_URL,'categories.txt')
XPPKG_CATEGORIES = urllib.urlopen(XPPKG_CATEGORIES_URL).read().split('\n')

if __name__ == '__main__':
    discover_XPlane()

