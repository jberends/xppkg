# Meta data language of XPpkg packages

Status: In preparation


## Background

The background of the metadata description of XPpkg packages is based on the distribution system of Pyhton Packages.
The PIP314 [http://www.python.org/dev/peps/pep-0314/] is used for main inspiration.

## Fields


    Metadata-Version -- The version of the standard in use 1.0 is current
    Package -- the package name
    Version -- the package version (according to http://epydoc.sourceforge.net/stdlib/distutils.version-module.html)
    Architecture -- architecture the package is for
        Win,Mac,Linux
    Author -- contact name of package maker (required with Author-Email)
    Author-Email -- contact email of the package maker (required with Author)
    Depends -- declares an absolute dependency
        X-Plane>10 (X-plane is in this sense a virtual package)
    Recommends -- declares a strong but not absolute dependency
    Suggests -- recommends other packages to install
    Pre-Depends -- declares an installation dependency
    Conflicts -- says what this cannot coexist with
    Replaces -- declares that this replaces given packages (not versions)
    Provides -- declares `virtual' packages for dependency purposes
    Description -- multiline description of package.
    Section -- application area of the package
        Aircraft
        Livery
        Scenery
        Plugin
        Navdata
    Installed-Size -- installed size of the package (optional, calculated)
    Date -- last-modified-date of metadata
    Changes -- human-readable changelog data (optional)
    Size -- size of binary package (optional, calculated)
    MD5sum -- MD5 checksum of the package (optional, calculated)
    License -- The license statement for the package

    [source: PyPi additional key:value for installation]
    ReleaseURL -- The URL where to obtain the original ZIP package.


### Metadata-Version (required)

  Version of the file format; currently "1.0" is the only legal values here.

  Example:
       Metadata-Version: 1.0

### Name (required)

  The name of the package. This name is unique in the world of packages for X-Plane and is case sensitive
  It is a 'slug' meaning should contain lowercase characters and can only include a 'minus' or 'hyphen'

  Example:

      Name: Columbia400
      Name: Boeing-747

### Version (required)

  A string containing the package's version number. This field should be parseable by one of the Version classes
  (StrictVersion or LooseVersion) in the distutils.version module
  [http://epydoc.sourceforge.net/stdlib/distutils.version-module.html]

  Example:

      Version: 1.0a2

### Platform (multiple use)

  A comma-separated list of platform specifications, options can be 'Win', 'Mac' or 'Linux'

  Example:

      Platform: Mac
      Platform: Win
      Platform: [Mac, Win, Linux]

### Summary

  A one-line summary of what the package does.

  Example:

      Summary: A module for collecting votes from beagles.

### Description (optional)

  A longer description of the package that can run to several
  paragraphs.  Software that deals with metadata should not assume
  any maximum size for this field, though people shouldn't include
  their instruction manual as the description.

  The contents of this field can be written using reStructuredText
  markup [1].  For programs that work with the metadata,
  supporting markup is optional; programs can also display the
  contents of the field as-is.  This means that authors should be
  conservative in the markup they use.

  Example:

      Description: This module collects votes from beagles
                   in order to determine their electoral wishes.
                   Do *not* try to use this module with basset hounds;
                   it makes them grumpy.


### Home-page (optional)

  A string containing the URL for the package's home page.

  Example:

      Home-page: http://www.example.com/~cschultz/bvote/

### Download-URL

  A string containing the URL from which this version of the package
  can be downloaded.  (This means that the URL can't be something like
  ".../package-latest.tgz", but instead must be "../package-0.45.tgz".)

### Author (optional, required with Author-Email)

  A string containing the author's name at a minimum; additional
  contact information may be provided.

  Example:

      Author: Jochem Berends

### Author-Email (optional, required with Author)

  A string containing the author's e-mail address.  It can contain
  a name and e-mail address in the legal forms for a RFC-822
  'From:' header.  It's not optional because cataloging systems
  can use the e-mail portion of this field as a unique key
  representing the author.  A catalog might provide authors the
  ability to store their GPG key, personal home page, and other
  additional metadata *about the author*, and optionally the
  ability to associate several e-mail addresses with the same
  person.

  Example:

      Author-email: jberends+xppkg@jbits.nl
      Author-email: Jochem Berends <jberends+xppkg@jbits.nl>

### License

  Text indicating the license covering the package where the license
  is not a selection from the "License" Trove classifiers. See
  "Classifier" below.

  Example:

      License: This software may only be obtained by sending the
               author a postcard, and then the user promises not
               to redistribute it.

### Classifier (multiple use)

  Each entry is a string giving a single classification value
  for the package.  Classifiers are described in PEP 301 [2].

  Examples:

    Classifier: Development Status :: 4 - Beta
    Classifier: Environment :: Console (Text Based)


### Requires (multiple use)

  Each entry contains a string describing some other module or
  package required by this package.

  The format of a requirement string is identical to that of a
  module or package name usable with the 'import' statement,
  optionally followed by a version declaration within parentheses.

  A version declaration is a series of conditional operators and
  version numbers, separated by commas.  Conditional operators
  must be one of "<", ">", "<=", ">=", "==", and "!=".  Version
  numbers must be in the format accepted by the
  distutils.version.StrictVersion class: two or three
  dot-separated numeric components, with an optional "pre-release"
  tag on the end consisting of the letter 'a' or 'b' followed by a
  number.  Example version numbers are "1.0", "2.3a2", "1.3.99",

  Any number of conditional operators can be specified, e.g.
  the string ">1.0, !=1.3.4, <2.0" is a legal version declaration.

  All of the following are possible requirement strings: "rfc822",
  "zlib (>=1.1.4)", "zope".

  There's no canonical list of what strings should be used; the
  Python community is left to choose its own standards.

  Example:

      Requires: re
      Requires: sys
      Requires: zlib
      Requires: xml.parsers.expat (>1.0)
      Requires: psycopg

### Provides (multiple use)

  Each entry contains a string describing a package or module that
  will be provided by this package once it is installed.  These
  strings should match the ones used in Requirements fields.  A
  version declaration may be supplied (without a comparison
  operator); the package's version number will be implied if none
  is specified.

  Example:

      Provides: xml
      Provides: xml.utils
      Provides: xml.utils.iso8601
      Provides: xml.dom
      Provides: xmltools (1.3)

### Obsoletes (multiple use)

  Each entry contains a string describing a package or module
  that this package renders obsolete, meaning that the two packages
  should not be installed at the same time.  Version declarations
  can be supplied.

  The most common use of this field will be in case a package name
  changes, e.g. Gorgon 2.3 gets subsumed into Torqued Python 1.0.
  When you install Torqued Python, the Gorgon package should be
  removed.

  Example:

      Obsoletes: Gorgon


## References

[1] reStructuredText http://docutils.sourceforge.net/

[2] PEP 301 http://www.python.org/dev/peps/pep-0301/