import platform

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

