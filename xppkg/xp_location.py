"""
Finds the X-SYSTEM location depending on your environment
"""
import platform

XSYSTEM_LOCATION_HELPERS={
    'Darwin':'/Applications/X-Plane 10',
    'Win':'C:/Program Files/X-Plane 10',
    'Linux':'/opt/X-plane 10'
}

XPLANE_VERSION_CMD={
    'Darwin':'X-Plane.app/Contents/MacOS/X-Plane --version',
    'Win':'X-Plane.exe --version',
    'Linux':'X-Plane --version'
}

SYSTEM = platform.system()


