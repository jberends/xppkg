"""Exceptions used throughout package"""


class XPpkgError(Exception):
    """Base pip exception"""


class InstallationError(XPpkgError):
    """General exception during installation"""

class SimulatorNotInstalledError(XPpkgError):
    """General exception when the simulator is not found"""


class UninstallationError(XPpkgError):
    """General exception during uninstallation"""


class DistributionNotFound(InstallationError):
    """Raised when a distribution cannot be found to satisfy a requirement"""


class BestVersionAlreadyInstalled(XPpkgError):
    """Raised when the most up-to-date version of a package is already
    installed.  """


class BadCommand(XPpkgError):
    """Raised when virtualenv or a command is not found"""


class CommandError(XPpkgError):
    """Raised when there is an error in command-line arguments"""
