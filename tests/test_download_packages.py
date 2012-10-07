# nosetest
# source: https://nose.readthedocs.org/en/latest/writing_tests.html
import os
from nose import with_setup
from xppkg import util
from xppkg.index import Link
from xppkg.download import unpack_http_url

from xppkg.settings import XPPKG_POOL_URL

_test_aircraft_url = 'https://github.com/jberends/xppkg/blob/master/packages/pool/test-aircraft-1.1.zip?raw=true'
_test_scenery_url = 'https://github.com/jberends/xppkg/blob/master/packages/pool/test-scenery-1.0.zip?raw=true'
_pool_url = XPPKG_POOL_URL
_cwd = os.getcwd()
_tempo_test_dir = os.path.join(_cwd, '_testing')

def setup_func():
    """set up test fixtures"""
    if os.path.isdir(_tempo_test_dir):
        if os.path.isdir(util.backup_dir(_tempo_test_dir)):
            os.removedirs(util.backup_dir(_tempo_test_dir))
        os.rename(_tempo_test_dir, util.backup_dir(_tempo_test_dir))

def teardown_func():
    """tear down test fixtures"""
    pass

@with_setup(setup_func, teardown_func)
def test_download_aircraft():
    """
    This test the download from the URL repository
    """
    download_url = _test_aircraft_url
    download_link = Link(download_url)
    location = os.path.join(_tempo_test_dir,'Aircraft','Test Aircraft')

    unpack_http_url(download_link, location, download_cache=None, download_dir=None)

@with_setup(setup_func, teardown_func)
def test_download_scenery():
    """
    This test the download from the URL repository
    """
    download_url = _test_scenery_url
    download_link = Link(download_url)
    location = os.path.join(_tempo_test_dir,'Scenery','Test Scenery')

    unpack_http_url(download_link, location, download_cache=None, download_dir=None)



