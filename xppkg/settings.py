"""
Finds the X-SYSTEM location depending on your environment, bootstraps the settings
"""

import platform
import os
import util
import exceptions

# For debugging purposes in testing phase
DEBUG = True

XSYSTEM_LOCATION_HELPERS={
    'Darwin':'/Applications/X-Plane 10/',
    'Win':'C:/Program Files/X-Plane 10/',
    'Linux':'/opt/X-plane 10'
}

XPLANE_EXECUTABLE={
    'Darwin': 'X-Plane.app/Contents/MacOS/X-Plane',
    'Win':'X-plane.exe',
    'Linux':'X-plane'
}

INSTALLATION_LOG='/Output/preferences/directory.txt'

SYSTEM = platform.system()
XSYSTEM_PATH = ''
XSYSTEM_VERSION = ''

# Ignored file patterns in the snap
SNAP_IGNORED_PATTERNS = ['.DS_Store','*.svn*', '*.git*', '*.png','*.gif' ]
if DEBUG:
    SNAP_IGNORED_PATTERNS.extend(['*.dsf','*.osf','*.osm','*.acf','*.wav','*.afl','*.txt','*.pdf',
                                  '*.obj','*.ter','*.pol','*.for','*.dds','*.wpn','*.bmp'])

"""
Bootstraps by discovering the XSYSTEM_PATH and XSYSTEM_VERSION
"""
# set XSYSTEM_PATH this is a happy path, no searching
if os.path.exists(XSYSTEM_LOCATION_HELPERS[SYSTEM]) and\
   os.path.isfile(os.path.join(XSYSTEM_LOCATION_HELPERS[SYSTEM],
       XPLANE_EXECUTABLE[SYSTEM])):
    XSYSTEM_PATH = os.path.dirname(XSYSTEM_LOCATION_HELPERS[SYSTEM])
else:
    raise exceptions.SimulatorNotInstalledError,\
    ('Cannot find X-Plane installation at %s' % XSYSTEM_LOCATION_HELPERS[SYSTEM])

# set XSYSTEM_VERSION
get_version_cmd = [os.path.join(XSYSTEM_PATH,
    XPLANE_EXECUTABLE[SYSTEM]), '--version']
XSYSTEM_VERSION = util.call_subprocess(get_version_cmd, show_stdout=False)

if __name__ == '__main__':
    pass

