"""
Finds the X-SYSTEM location depending on your environment
"""

XSYSTEM_LOCATION_HELPERS={
    'Darwin':'file://Applications/X-Plane 10',
    'Win':'file://C:/Program Files/X-Plane 10',
    'Linux':'file://opt/X-plane 10'
}

XPLANE_VERSION_CMD={
    'Darwin':'X-Plane.app/Contents/MacOS/X-Plane --version',
    'Win':'X-Plane.exe --version',
    'Linux':'X-Plane --version'
}
