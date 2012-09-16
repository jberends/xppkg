"""
Takes snapshot of a directory and stores that inside a YAML file
"""
import fnmatch
import os
import yaml
import settings, util
from log import logger

SNAPSHOT_PATHNAME = 'snap.yml'

import time

def timeit(method):

    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        logger.debug('%r (%r, %r) %2.2f sec' %\
              (method.__name__, args, kw, te-ts))
        return result

    return timed

@timeit
def snapshot(path=None, ignore_filters=None, calculate_md5=False):
    """
    makes a snapshot of the X-plane environment and stores this inside a YAML file

    add md5 sum to every file is requested
    """
    path = path or os.getcwd()
    snap = {}
    dirpaths = []
    logger.notify('Starting the snapshot')
    if ignore_filters:
        logger.notify('Ignoring filenames with filters: %s' % ignore_filters)
    for dirpath, dirnames, filenames in os.walk(path):
        if ignore_filters:
            # get myself a list of files that are ignored
            ignored_filenames = []
            ignored_filenames.extend(
                [fnmatch.filter(filenames, filter.lower()) for filter in ignore_filters])
            # flatten list
            ignored_filenames = [item for sublist in ignored_filenames for item in sublist]
            filenames = [fn for fn in filenames if fn not in ignored_filenames]
        if len(dirpath) > 80:
            logger.notify('snapping %i files in %s.. ..%s' % (len(filenames), dirpath[:25], dirpath[-45:]))
        else:
            logger.notify('snapping %i files in %s' % (len(filenames), dirpath))
        if len(filenames) >= 1 and not [fnmatch.fnmatch(dirpath, filter) for filter in ignore_filters]:
        #if len(filenames) >= 1:
            if calculate_md5:
                filenames_with_md5 = []
                for fn in filenames:
                    hashsum = str(util.get_file_hash(os.path.join(dirpath,fn)))
                    filenames_with_md5.append( {fn: hashsum} )
                snap.update({dirpath: filenames_with_md5})
        else:
            snap.update({dirpath: filenames})
        dirpaths.append(dirpath)
    return snap



if __name__ == '__main__':
    snap = snapshot(settings.XSYSTEM_PATH, ignore_filters=settings.SNAP_IGNORED_PATTERNS, calculate_md5=True)
    #snap = snapshot(os.getcwd(), ignore_filters=['__*__.py','*.pyc'], calculate_md5=True)
    yaml.dump(snap, open(SNAPSHOT_PATHNAME, 'w'))

