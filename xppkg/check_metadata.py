"""
Checks the Metadata
"""
import email.utils
import re
from exceptions import MetaDataError

class MetaData(object):
    """
    The metadata class (which is in fact a dict)
    """

    _metadata = {}

    def __init__(self, metadata):
        self._metadata = metadata

    def normalise_metadata(self):
        """
        Normalises the Metadata. Will remove all capitals from the keys
        """
        metadata = {}
        for key in self._metadata.keys():
            metadata[key.lower().strip()] = self._metadata[key]
        self._metadata = metadata


METADATA_KEYS = [key.title() for key in [
    'Metadata-Version', 'Package', 'Version', 'Architecture', 'Author', 'Depends', 'Recommends',
    'Suggests', 'Pre-Depends', 'Conflicts', 'Replaces', 'Provides', 'Description', 'Section',
    'Installed-Size', 'Date', 'Changes', 'Size', 'Md5sum', 'License', 'Author-Email', 'Download-Url',
    'Package-Url','Home-Page', 'Categories'
]]
METADATA_KEYS_REQUIRED = ['Metadata-Version', 'Package', 'Version']
METADATA_VERSION = str(1.0)
METADATA_ARCHITECTURES = ['Win','Mac','Linux']
METADATA_SECTIONS = ['Aircraft','Scenery','Plugin','Livery','Navdata']
METADATA_EMAIL_REGEX = r'([A-Za-z0-9_\.\+-]+)@([\da-z\.-]+)\.([a-z\.]{2,6})'


def check_metadata(metadata):
    """
    checks the metadata, returns the cleaned dict

    does not read the metadata file, expects a dict (yaml.Dict) object
    """
    # check if of type dict
    assert type(metadata) == dict

    # check if keys are 'known keys'
    metadata = _normalise_metadatakeys(metadata)
    for key in metadata.keys():
        try:
            assert key in METADATA_KEYS
        except AssertionError:
            raise MetaDataError, "Key '%s' not known in the list of allowed keys in the Metadata" % key

    # check if the meta-data has at least the required keys
    for required_key in METADATA_KEYS_REQUIRED:
        if required_key not in metadata.keys():
            raise MetaDataError, "Could not find key '%s' in the package metadata \n%r" \
                                 % (required_key, metadata.keys())

    #TODO: refactor out of the checker function, into the cleaner function of the MetaData object
    if type(metadata['Metadata-Version']) is float:
        metadata['Metadata-Version'] = str(metadata['Metadata-Version'])
    if type(metadata['Version']) is float:
        metadata['Version'] = str(metadata['Version'])

    # check Metadata-Version
    if not (metadata['Metadata-Version'] == METADATA_VERSION):
        raise MetaDataError, "The Metadata-Version found is of type '%r' and '%s' while version '%s' is in effect"\
                             % (type(metadata['Metadata-Version']),metadata['Metadata-Version'] , METADATA_VERSION)

    # check if Architecture is there, and when there if it is a list and if the listitems conforms to the allowed list
    if 'Architecture' in metadata:
        if type(metadata['Architecture']) is list:
            for arch in metadata['Architecture']:
                arch = arch.strip().title()
                if arch not in METADATA_ARCHITECTURES:
                    raise MetaDataError, "The Architecture '%s' is not known in the list of architectures (%s)" \
                                         % (arch, METADATA_ARCHITECTURES)
        elif type(metadata['Architecture']) is str:
            arch = metadata['Architecture']
            arch = arch.strip().title()
            if arch not in METADATA_ARCHITECTURES:
                raise MetaDataError, "The Architecture '%s' is not known in the list of architectures (%s)"\
                                     % (arch, METADATA_ARCHITECTURES)
        else:
            raise MetaDataError, "The Architecture '%s' is of unknown type or unreadable" % metadata['Architecture']

    # check if section exist, if it conforms to the allowed list of sections
    if 'Section' in metadata:
        if type(metadata['Section']) is str:
            section = metadata['Section']
            section = section.strip().title()
            if section not in METADATA_SECTIONS:
                raise MetaDataError, "The Section '%s' is not known in the list of sections (%s)" \
                                     % (section, METADATA_SECTIONS)

    # Check for Author and Author-Email, check if the Email is an Email address regex
    if 'Author' in metadata and not 'Author-Email' in metadata:
        raise MetaDataError, "When Author is provided, the Author-Email should be provided too"
    elif not 'Author' in metadata and 'Author-Email' in metadata:
        raise MetaDataError, "When Author-Email is provided, the Author should be provided too"
    elif 'Author' in metadata and 'Author-Email' in metadata:
        if type(metadata['Author']) is not str:
            raise MetaDataError, "Author is not a string '%s'" % metadata['Author']
        if type(metadata['Author-Email']) is not str:
            raise MetaDataError, "Author's Email is not a string '%s'" % metadata['Author']
        author_email = metadata['Author-Email']
        # check against RFC822 using email.utils.parseaddr
        _, his_email = email.utils.parseaddr(author_email)
        if not re.match(METADATA_EMAIL_REGEX, his_email):
            raise MetaDataError, "Author's email '%s' seems not to be a correct formatted email address (%s)"\
                                 % (his_email, metadata['Author-Email'])


def _normalise_metadatakeys(dict_in):
    """Normalises the keys in a dict_in to become lower case and without whitespaces, whitespace is replaced with _"""
    new_dict = {}
    for key in dict_in.keys():
        new_key = key.strip().title().replace('_','-').replace(' ','-')
        new_dict[new_key] = dict_in[key]
    return new_dict
