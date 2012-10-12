# borrowed some util functions from the pip project. (http://www.pip-installer.org)
# that code is written under the MIT license, copyright by the pip-developers
import os
import platform
import re
import shutil
import tarfile
import time
import subprocess
import sys
import posixpath
import zipfile
from backwardcompat import console_to_str
from log import logger
import hashlib

#######
# pip utils
#######

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
            raise Exception(
                "Command %s failed with error code %s in %s"
                % (command_desc, proc.returncode, cwd))
        else:
            logger.warn(
                "Command %s had error code %s in %s"
                % (command_desc, proc.returncode, cwd))
    if stdout is not None:
        return ''.join(all_output)

def get_file_hash(filename):
    """
    gets a hash from a file using a hash_algorithm.
    hash_algoritm implemented is 'md5'

    >>> get_file_hash('__init__.py')
    46564
    """
    hash = hashlib.md5()
    with open(filename,'rb', 8192) as f:
        for chunk in iter(lambda: f.read(8192), b''):
            hash.update(chunk)
    return hash.hexdigest()

def create_download_cache_folder(folder):
    logger.indent -= 2
    logger.notify('Creating supposed download cache at %s' % folder)
    logger.indent += 2
    os.makedirs(folder)

def cache_download(target_file, temp_location, content_type):
    logger.notify('Storing download in cache at %s' % display_path(target_file))
    shutil.copyfile(temp_location, target_file)
    fp = open(target_file+'.content-type', 'w')
    fp.write(content_type)
    fp.close()
    os.unlink(temp_location)

def backup_dir(dir, ext='.bak'):
    """Figure out the name of a directory to back up the given dir to
    (adding .bak, .bak2, etc)"""
    n = 1
    extension = ext
    while os.path.exists(dir + extension):
        n += 1
        extension = ext + str(n)
    return dir + extension

def ask_path_exists(message, options):
    for action in os.environ.get('XPPKG_EXISTS_ACTION', ''):
        if action in options:
            return action
    return ask(message, options)

def ask(message, options):
    """Ask the message interactively, with the given possible responses"""
    while 1:
        if os.environ.get('XPPKG_NO_INPUT'):
            raise Exception('No input was expected ($XPPKG_NO_INPUT set); question: %s' % message)
        response = raw_input(message)
        response = response.strip().lower()
        if response not in options:
            print('Your response (%r) was not one of the expected responses: %s' % (
                response, ', '.join(options)))
        else:
            return response

def splitext(path):
    """Like os.path.splitext, but take off .tar too"""
    base, ext = posixpath.splitext(path)
    if base.lower().endswith('.tar'):
        ext = base[-4:] + ext
        base = base[:-4]
    return base, ext

def format_size(bytes):
    if bytes > 1000*1000:
        return '%.1fMB' % (bytes/1000.0/1000)
    elif bytes > 10*1000:
        return '%ikB' % (bytes/1000)
    elif bytes > 1000:
        return '%.1fkB' % (bytes/1000.0)
    else:
        return '%ibytes' % bytes

def display_path(path):
    """Gives the display value for a given path, making it relative to cwd
    if possible."""
    path = os.path.normcase(os.path.abspath(path))
    if path.startswith(os.getcwd() + os.path.sep):
        path = '.' + path[len(os.getcwd()):]
    return path

def is_svn_page(html):
    """Returns true if the page appears to be the index page of an svn repository"""
    return (re.search(r'<title>[^<]*Revision \d+:', html)
            and re.search(r'Powered by (?:<a[^>]*?>)?Subversion', html, re.I))

def file_contents(filename):
    fp = open(filename, 'rb')
    try:
        return fp.read().decode('utf-8')
    finally:
        fp.close()

def split_leading_dir(path):
    path = str(path)
    path = path.lstrip('/').lstrip('\\')
    if '/' in path and (('\\' in path and path.find('/') < path.find('\\'))
                        or '\\' not in path):
        return path.split('/', 1)
    elif '\\' in path:
        return path.split('\\', 1)
    else:
        return path, ''


def has_leading_dir(paths):
    """Returns true if all the paths have the same leading path name
    (i.e., everything is in one subdirectory in an archive)"""
    common_prefix = None
    for path in paths:
        prefix, rest = split_leading_dir(path)
        if not prefix:
            return False
        elif common_prefix is None:
            common_prefix = prefix
        elif prefix != common_prefix:
            return False
    return True

def unpack_file(filename, location, content_type, link):
    if (content_type == 'application/zip'
        or filename.endswith('.zip')
        or filename.endswith('.pybundle')
        or zipfile.is_zipfile(filename)):
        unzip_file(filename, location, flatten=not filename.endswith('.pybundle'))
    elif (content_type == 'application/x-gzip'
          or tarfile.is_tarfile(filename)
          or splitext(filename)[1].lower() in ('.tar', '.tar.gz', '.tar.bz2', '.tgz', '.tbz')):
        untar_file(filename, location)
    elif (content_type and content_type.startswith('text/html')
          and is_svn_page(file_contents(filename))):
        # We don't really care about this
        from pip.vcs.subversion import Subversion
        Subversion('svn+' + link.url).unpack(location)
    else:
        ## FIXME: handle?
        ## FIXME: magic signatures?
        logger.fatal('Cannot unpack file %s (downloaded from %s, content-type: %s); cannot detect archive format'
                     % (filename, location, content_type))
        raise exceptions.InstallationError('Cannot determine archive format of %s' % location)

def unzip_file(filename, location, flatten=True):
    """Unzip the file (zip file located at filename) to the destination
    location"""
    if not os.path.exists(location):
        os.makedirs(location)
    zipfp = open(filename, 'rb')
    try:
        zip = zipfile.ZipFile(zipfp)
        leading = has_leading_dir(zip.namelist()) and flatten
        for name in zip.namelist():
            data = zip.read(name)
            fn = name
            if leading:
                fn = split_leading_dir(name)[1]
            fn = os.path.join(location, fn)
            dir = os.path.dirname(fn)
            if not os.path.exists(dir):
                os.makedirs(dir)
            if fn.endswith('/') or fn.endswith('\\'):
                # A directory
                if not os.path.exists(fn):
                    os.makedirs(fn)
            else:
                fp = open(fn, 'wb')
                try:
                    fp.write(data)
                finally:
                    fp.close()
    finally:
        zipfp.close()


def untar_file(filename, location):
    """Untar the file (tar file located at filename) to the destination location"""
    if not os.path.exists(location):
        os.makedirs(location)
    if filename.lower().endswith('.gz') or filename.lower().endswith('.tgz'):
        mode = 'r:gz'
    elif filename.lower().endswith('.bz2') or filename.lower().endswith('.tbz'):
        mode = 'r:bz2'
    elif filename.lower().endswith('.tar'):
        mode = 'r'
    else:
        logger.warn('Cannot determine compression type for file %s' % filename)
        mode = 'r:*'
    tar = tarfile.open(filename, mode)
    try:
        # note: python<=2.5 doesnt seem to know about pax headers, filter them
        leading = has_leading_dir([
        member.name for member in tar.getmembers()
        if member.name != 'pax_global_header'
        ])
        for member in tar.getmembers():
            fn = member.name
            if fn == 'pax_global_header':
                continue
            if leading:
                fn = split_leading_dir(fn)[1]
            path = os.path.join(location, fn)
            if member.isdir():
                if not os.path.exists(path):
                    os.makedirs(path)
            elif member.issym():
                try:
                    tar._extract_member(member, path)
                except:
                    e = sys.exc_info()[1]
                    # Some corrupt tar files seem to produce this
                    # (specifically bad symlinks)
                    logger.warn(
                        'In the tar file %s the member %s is invalid: %s'
                        % (filename, member.name, e))
                    continue
            else:
                try:
                    fp = tar.extractfile(member)
                except (KeyError, AttributeError):
                    e = sys.exc_info()[1]
                    # Some corrupt tar files seem to produce this
                    # (specifically bad symlinks)
                    logger.warn(
                        'In the tar file %s the member %s is invalid: %s'
                        % (filename, member.name, e))
                    continue
                if not os.path.exists(os.path.dirname(path)):
                    os.makedirs(os.path.dirname(path))
                destfp = open(path, 'wb')
                try:
                    shutil.copyfileobj(fp, destfp)
                finally:
                    destfp.close()
                fp.close()
    finally:
        tar.close()

class _Inf(object):
    """I am bigger than everything!"""

    def __eq__(self, other):
        if self is other:
            return True
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        return False

    def __le__(self, other):
        return False

    def __gt__(self, other):
        return True

    def __ge__(self, other):
        return True

    def __repr__(self):
        return 'Inf'

Inf = _Inf()
del _Inf

#######
# XPPKG own utils
#######

def timeit(method):

    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        logger.debug('%r (%r, %r) %2.2f sec' %\
                     (method.__name__, args, kw, te-ts))
        return result
    return timed


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