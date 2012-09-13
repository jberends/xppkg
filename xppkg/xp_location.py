"""
Finds the X-SYSTEM location depending on your environment
"""
import glob
import os
import platform
from xppkg import util
from xppkg.exceptions import SimulatorNotInstalledError
from xppkg import settings


def bootstrap():
    """
    Bootstraps by discovering the settings.XSYSTEM_PATH and settings.XSYSTEM_VERSION
    """
    # set settings.XSYSTEM_PATH this is a happy path, no searching
    if os.path.exists(settings.XSYSTEM_LOCATION_HELPERS[settings.SYSTEM]) and \
    os.path.isfile(os.path.join(settings.XSYSTEM_LOCATION_HELPERS[settings.SYSTEM],
                                settings.XPLANE_EXECUTABLE[settings.SYSTEM])):
        settings.XSYSTEM_PATH = os.path.dirname(settings.XSYSTEM_LOCATION_HELPERS[settings.SYSTEM])
    else:
        raise SimulatorNotInstalledError, \
            ('Cannot find X-Plane installation at %s' % settings.XSYSTEM_LOCATION_HELPERS[settings.SYSTEM])

    # set settings.XSYSTEM_VERSION
    get_version_cmd = [os.path.join(settings.XSYSTEM_PATH,
        settings.XPLANE_EXECUTABLE[settings.SYSTEM]),'--version']
    settings.XSYSTEM_VERSION = util.call_subprocess(get_version_cmd, show_stdout=False)




def find_files(pathpattern):
    """
    Find files on disk

    pathpattern = matching a specified pattern according to the rules used by the Unix shell

    >>> find_files('*init_?.py')
    ['__init__.py']
    """
    return glob.glob(pathpattern)

if __name__ == '__main__':
    bootstrap()
    pass
