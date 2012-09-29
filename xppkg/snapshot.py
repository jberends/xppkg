"""
Takes snapshot of a directory and stores that inside a YAML file
"""
import fnmatch
import os
import  util
from log import logger

SNAPSHOT_PATHNAME = 'snap.yml'



@util.timeit
def snapshot(path=None, ignore_filters=None, md5=False, size=False, datetime=False):
    """ makes a snapshot of the X-plane environment and stores this inside a YAML file
    add md5 sum to every file is requested
    you may provide a list of filepatterns to ignore

    >>> snapshot(os.getwcwd())
    []
    # test2 with ignores (wildcards)
    >>> snapshot(os.getcwd(), ignore_filters=['__*__.py','*.pyc'])
    []
    # test3 without ignores with sizes
    >>> snapshot(os.getcwd(), size=True)
    []
    # test4 with ignores and sizes
    >>> snapshot(os.ignore_filters=['__*__.py','*.pyc'], size=True)
    []
    # test4 with ignores and md5
    >>> snapshot(os.ignore_filters=['__*__.py','*.pyc'], md5=True)
    []
    # test6 everything
    >>> snapshot(os.ignore_filters=['__*__.py','*.pyc'], md5=True, size=True)
    []

    :type datetime: bool
    :type ignore_filters: list
    :type size: bool
    :type md5: bool
    """

    path = path or os.getcwd()
    snap = {}
    dirpaths = []

    if not os.path.isdir(path):
        raise IOError, ('Directory %s not found, unable to make a snapshot of it', path)

    logger.notify('Starting the snapshot')
    if ignore_filters:
        logger.notify('Ignoring filenames with filters: %s' % ignore_filters)
    for dirpath, dirnames, filenames in os.walk(path):
        if ignore_filters and [fnmatch.fnmatch(dirpath, filter) for filter in ignore_filters]:
            if dirpath not in snap:
                snap.update({dirpath: {}})
            # do filtering first
            if ignore_filters:
                # get myself a list of files that are ignored
                ignored_filenames = []
                ignored_filenames.extend(
                    [fnmatch.filter(filenames, filter.lower()) for filter in ignore_filters])
                # flatten list
                ignored_filenames = [item for sublist in ignored_filenames for item in sublist]
                filenames = [fn for fn in filenames if fn not in ignored_filenames]
            # filenames are now cleaned and rinsed
            if dirpath is not None and len(dirpath) > 80:
                logger.notify('snapping %i files in %s.. ..%s' % (len(filenames), dirpath[:25], dirpath[-45:]))
            else:
                logger.notify('snapping %i files in %s' % (len(filenames), dirpath))

            # do the actual snapping and sizing and md5-ing here
            if len(filenames) >= 1:
                if md5:
                    for fn in filenames:
                        hashsum = str(util.get_file_hash(os.path.join(dirpath,fn)))
                        if fn in snap[dirpath]:
                            snap[dirpath][fn].update({'md5':hashsum})
                        else:
                            snap[dirpath].update({fn: {'md5':hashsum}})
                if size:
                    filesizes = []
                    for fn in filenames:
                        filesize = os.path.getsize(os.path.join(dirpath,fn))
                        if fn in snap[dirpath]:
                            snap[dirpath][fn].update({'size':filesize})
                        else:
                            snap[dirpath].update({fn: {'size':filesize}})
                        filesizes.append(filesize)
                    snap[dirpath].update({'DIR_SIZE': sum(filesizes)})
                if datetime:
                    for fn in filenames:
                        if fn in snap[dirpath]:
                            snap[dirpath][fn].update({'modified_on':getmtime(os.path.join(dirpath, fn))})
                if not md5 and not size and not datetime:
                    snap[dirpath] = filenames
    return snap



if __name__ == '__main__':
    #snap = snapshot(settings.XSYSTEM_PATH, ignore_filters=settings.SNAP_IGNORED_PATTERNS, calculate_md5=True)
    #snap = snapshot(os.getcwd(), ignore_filters=['__*__.py','*.pyc'], calculate_md5=True)
    #yaml.dump(snap, open(SNAPSHOT_PATHNAME, 'w'))

    #snaped = yaml.load(open(SNAPSHOT_PATHNAME))

    dist_path = '/Users/jochem/Downloads/OpenSceneryX'
    #snap = snapshot(dist_path, calculate_size=True)
    snap = snapshot(os.getcwd(), ignore_filters=['__*__.py','*.pyc','*.git*'], size=True)
    pass
