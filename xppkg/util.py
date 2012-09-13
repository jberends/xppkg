# borrowed some util functions from the pip project. (http://www.pip-installer.org)
# that code is written under the MIT license, copyright by the pip-developers
import os

import subprocess
import sys
from exceptions import InstallationError
from backwardcompat import console_to_str
from log import logger

def call_subprocess(cmd,
                    show_stdout=True,
                    filter_stdout=None,
                    cwd=None,
                    raise_on_returncode=True,
                    command_level=logger.DEBUG,
                    command_desc=None,
                    extra_environ=None):
    """
    Uses subprocess to call a cmd with some handling
    """
    if command_desc is None:
        cmd_parts = []
        for part in cmd:
            if ' ' in part or '\n' in part or '"' in part or "'" in part:
                part = '"%s"' % part.replace('"', '\\"')
            cmd_parts.append(part)
        command_desc = ' '.join(cmd_parts)
    if show_stdout:
        stdout = None
    else:
        stdout = subprocess.PIPE
    logger.log(command_level, "Running command %s" % command_desc)
    env = os.environ.copy()
    if extra_environ:
        env.update(extra_environ)
    try:
        proc = subprocess.Popen(
            cmd, stderr=subprocess.STDOUT, stdin=None, stdout=stdout,
            cwd=cwd, env=env)
    except Exception:
        e = sys.exc_info()[1]
        logger.fatal(
            "Error %s while executing command %s" % (e, command_desc))
        raise
    all_output = []
    if stdout is not None:
        stdout = proc.stdout
        while 1:
            line = console_to_str(stdout.readline())
            if not line:
                break
            line = line.rstrip()
            all_output.append(line + '\n')
            if filter_stdout:
                level = filter_stdout(line)
                if isinstance(level, tuple):
                    level, line = level
                logger.log(level, line)
                if not logger.stdout_level_matches(level):
                    logger.show_progress()
            else:
                logger.info(line)
    else:
        returned_stdout, returned_stderr = proc.communicate()
        all_output = [returned_stdout or '']
    proc.wait()
    if proc.returncode:
        if raise_on_returncode:
            if all_output:
                logger.notify('Complete output from command %s:' % command_desc)
                logger.notify('\n'.join(all_output) + '\n----------------------------------------')
            raise InstallationError(
                "Command %s failed with error code %s in %s"
                % (command_desc, proc.returncode, cwd))
        else:
            logger.warn(
                "Command %s had error code %s in %s"
                % (command_desc, proc.returncode, cwd))
    if stdout is not None:
        return ''.join(all_output)
