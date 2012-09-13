"""
Takes snapshot of a directory and stores that inside a YAML file
"""
import os
from xppkg import settings

SNAPSHOT_PATHNAME = 'snap.yml'

def snapshot(path=None):
    """
    makes a snapshot of the X-plane environment and stores this inside a YAML file
    """
    path = path or os.getcwd()

    snap = {}
    dirpaths = []
    for dirpath, dirnames, filenames in os.walk(path):
        snap.update({dirpath: filenames})
        dirpaths.append(dirpath)

    return snap, dirpaths



if __name__ == '__main__':
    import xp_location
    xp_location.bootstrap()
    snap, dirpaths = snapshot(settings.XSYSTEM_PATH)
    print settings.XSYSTEM_PATH
    pass


