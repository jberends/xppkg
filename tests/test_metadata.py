import os
from pprint import pprint
import unittest
import yaml

from xppkg.check_metadata import check_metadata
from xppkg.exceptions import MetaDataError

_metadata_aircraft_filename = os.path.join(os.path.dirname(__file__), 'test-packages', 'test-aircraft-1.0.yaml')
_metadata_scenery_filename = os.path.join(os.path.dirname(__file__), 'test-packages', 'test-scenery-1.0.yaml')


class TestMetadataFiles(unittest.TestCase):
    def test_metadata_aircraft(self):
        """
        Test the metadata of a aircraft
        """
        assert os.path.exists(_metadata_aircraft_filename)
        metadata = yaml.load(open(_metadata_aircraft_filename))
        pprint(metadata)
        assert check_metadata(metadata)

    def test_metadata_scenery(self):
        """
        Test the metadata of a scenery
        """
        assert os.path.exists(_metadata_scenery_filename)
        metadata = yaml.load(open(_metadata_scenery_filename))
        pprint(metadata)
        assert check_metadata(metadata)


class TestMetaDataContents(unittest.TestCase):
    def setUp(self):
        self._metadata_base = {'Package': 'Test-package', 'Version': '1.0', 'Metadata-Version': '1.0'}

    def test_author(self):
        self._metadata_base['Author'] = 'An Author'
        self.assertRaises(MetaDataError, check_metadata, self._metadata_base)

    def test_metadata_authoremail(self):
        """
        Tests the various email forms and Author
        """
        md = self._metadata_base
        md['Author'] = 'An Author'
        md['Author-Email'] = 'An Author <anemail-address@somedomain.com.uk>'
        self.assertIsNotNone(check_metadata(md))

        md['Author-Email'] = 'some@email.addr'
        self.assertIsNotNone(check_metadata(md))

        md['Author-Email'] = 'some.email.without.at.sign.com'
        self.assertRaisesRegexp(MetaDataError, r'^Author.*email.*', check_metadata, md)

    def test_sections(self):
        """
        Tests the sections
        """
        md = self._metadata_base

        # happy path
        for section in ['Aircraft', 'Scenery', 'Plugin', 'Livery', 'Navdata']:
            md['Section'] = section
            self.assertIsNotNone(check_metadata(md))

        # unhappy
        md['Section'] = 'Foobar'
        self.assertRaisesRegexp(MetaDataError, r'^The Section.*is not known.*', check_metadata, md)

    def test_keywords(self):
        """
        Tests the various Keywords, and the various keyword capatilisation types
        """
        md = self._metadata_base

        # happy path
        for key in ['Depends', 'Recommends',
                    'Suggests', 'Pre-Depends', 'Conflicts', 'Replaces', 'Provides', 'Description', 'Section',
                    'Installed-Size', 'Date', 'Changes', 'Size', 'Md5sum', 'License', 'Download-Url',
                    'Package-Url', 'Home-Page', 'Categories']:
            md[key] = None
            self.assertIsNotNone(check_metadata(md))
            del md[key]

        md = self._metadata_base
        md['Architecture'] = 'Win'
        self.assertIsNotNone(check_metadata(md))

        # other paths
        md = self._metadata_base
        md['metadata-version'] = '1.0'
        self.assertIsNotNone(check_metadata(md))

        # spaces are replaced with '-', whitespace is trimmed, key is titlelised
        md = self._metadata_base
        md['MeTaData verSiON '] = '1.0'
        self.assertIsNotNone(check_metadata(md))

        # some keys are required
        for required_key in ['Metadata-Version', 'Package', 'Version']:
            md = self._metadata_base
            del md[required_key]
            try:
                check_metadata(md)
            except MetaDataError:
                #noinspection PyStatementEffect
                True

if __name__ == '__main__':
    unittest.main()
