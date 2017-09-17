"""
Checks the Metadata
"""
import email.utils
import re

from xppkg.exceptions import MetaDataError


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
    'Package-Url', 'Home-Page', 'Categories'
]]
METADATA_KEYS_REQUIRED = ['Metadata-Version', 'Package', 'Version']
METADATA_VERSION = str(1.0)
METADATA_ARCHITECTURES = ['Win', 'Mac', 'Linux']
METADATA_SECTIONS = ['Aircraft', 'Scenery', 'Plugin', 'Livery', 'Navdata']
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
        if key not in METADATA_KEYS:
            raise MetaDataError("Key '{}' not known in the list of allowed keys in the Metadata".format(key))

    # check if the meta-data has at least the required keys
    for required_key in METADATA_KEYS_REQUIRED:
        if required_key not in metadata.keys():
            raise MetaDataError(
                "Could not find key '{}' in the package metadata, found: {}".format(required_key, metadata.keys()))

    # TODO: refactor out of the checker function, into the cleaner function of the MetaData object
    if type(metadata['Metadata-Version']) is float:
        metadata['Metadata-Version'] = str(metadata['Metadata-Version'])
    if type(metadata['Version']) is float:
        metadata['Version'] = str(metadata['Version'])

    # check Metadata-Version
    if not (metadata['Metadata-Version'] == METADATA_VERSION):
        raise MetaDataError(
            "The Metadata-Version found is of type '{}' and '{}' while version '{}' is in effect".format(
                type(metadata['Metadata-Version']), metadata['Metadata-Version'], METADATA_VERSION))

    # check if Architecture is there, and when there if it is a list and if the listitems conforms to the allowed list
    if 'Architecture' in metadata:
        if type(metadata['Architecture']) is list:
            for arch in metadata['Architecture']:
                arch = arch.strip().title()
                if arch not in METADATA_ARCHITECTURES:
                    raise MetaDataError(
                        "The Architecture '{}' is not known in the list of architectures ({})".
                            format(arch, METADATA_ARCHITECTURES))
        elif isinstance(metadata['Architecture'], str):
            arch = metadata['Architecture']
            arch = arch.strip().title()
            if arch not in METADATA_ARCHITECTURES:
                raise MetaDataError("The Architecture '{}' is not known in the list of architectures ({})".
                                    format(arch, METADATA_ARCHITECTURES))
        else:
            raise MetaDataError(
                "The Architecture '{}' is of unknown type or unreadable".format(metadata['Architecture']))

    # check if section exist, if it conforms to the allowed list of sections
    if 'Section' in metadata:
        if type(metadata['Section']) is str:
            section = metadata['Section']
            section = section.strip().title()
            if section not in METADATA_SECTIONS:
                raise MetaDataError(
                    "The Section '{}' is not known in the list of sections ({})".format(section, METADATA_SECTIONS))

    # Check for Author and Author-Email, check if the Email is an Email address regex
    if 'Author' in metadata and not 'Author-Email' in metadata:
        raise MetaDataError("When Author is provided, the Author-Email should be provided too")
    elif not 'Author' in metadata and 'Author-Email' in metadata:
        raise MetaDataError("When Author-Email is provided, the Author should be provided too")
    elif 'Author' in metadata and 'Author-Email' in metadata:
        if type(metadata['Author']) is not str:
            raise MetaDataError("Author is not a string '{}'".format(metadata['Author']))
        if type(metadata['Author-Email']) is not str:
            raise MetaDataError("Author's Email is not a string '{}'".format(metadata['Author']))
        author_email = metadata['Author-Email']
        # check against RFC822 using email.utils.parseaddr
        _, the_email = email.utils.parseaddr(author_email)
        if not re.match(METADATA_EMAIL_REGEX, the_email):
            raise MetaDataError(
                "Author's email '{}' seems not to be a correct formatted email address ({})".
                    format(the_email, metadata['Author-Email']))

    # returns the 'cleaned' metadata
    return metadata


def _normalise_metadatakeys(dict_in):
    """Normalises the keys in a dict_in to become lower case and
    without whitespaces, whitespace is replaced with _"""
    new_dict = {}
    for key in dict_in.keys():
        new_key = key.strip().title().replace('_', '-').replace(' ', '-')
        new_dict[new_key] = dict_in[key]
    return new_dict
