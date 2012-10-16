# nosetest
# source: https://nose.readthedocs.org/en/latest/writing_tests.html
import os
from nose import with_setup
from pprint import pprint
import yaml
from xppkg.check_metadata import check_metadata

_metadata_aircraft_filename = os.path.join(os.path.dirname(__file__), 'test-packages', 'test-aircraft-1.0.yaml')
_metadata_scenery_filename = os.path.join(os.path.dirname(__file__), 'test-packages', 'test-scenery-1.0.yaml')


def setup_func():
    """set up test fixtures"""
    pass

def teardown_func():
    """tear down test fixtures"""
    pass

@with_setup(setup_func, teardown_func)
def test_metadata_aircraft():
    """
    Test the metadata of an aircraft
    """
    assert os.path.exists(_metadata_aircraft_filename)
    metadata = yaml.load(open(_metadata_aircraft_filename))
    pprint(metadata)
    check_metadata(metadata)

def test_metadata_scenery():
    """
    Test the metadata of an aircraft
    """
    assert os.path.exists(_metadata_scenery_filename)
    metadata = yaml.load(open(_metadata_scenery_filename))
    pprint(metadata)
    check_metadata(metadata)