# XPpkg repository

In this repository, the online information where to download various packages are provided. It is comparible
with the PyPi repository.

## Similarity from PyPi

PyPi uses various interface to communicate to the package database.
 * JSON [http://wiki.python.org/moin/PyPiJson]
 * XML-RPC [http://wiki.python.org/moin/PyPiXmlRpc]
 * HTTP [http://www.python.org/dev/peps/pep-0301/]


## XPpkg and Trove project

We aim to reuse knowledge that is already widely available in the community regarding package management.
The XPPKG-INF.yaml files use the yaml file format (to have it human readable) and contains classifiers from
the Trove project [http://www.catb.org/~esr/trove/trove-design-6.html]. Moveover PEP314 is used
[http://www.python.org/dev/peps/pep-0314/] for determination of the the key:value pairs used in
classification of the packages. Some modifications for X-Plane use is made.

The following key:value pair examples are handy

  Package Description
  [source: the Trove project]
    Metadata-Version -- The version of the standard in use 1.0 is current
    Package -- the package name
    Version -- the package version (according to http://epydoc.sourceforge.net/stdlib/distutils.version-module.html)
    Architecture -- architecture the package is for
        win,mac,linux
    Author -- contact email of package maker
    Depends -- declares an absolute dependency
        X-Plane > 10 (X-plane is in this sense a virtual package)
    Recommends -- declares a strong but not absolute dependency
    Suggests -- recommends other packages to install
    Pre-Depends -- declares an installation dependency
    Conflicts -- says what this cannot coexist with
    Replaces -- declares that this replaces given packages (not versions)
    Provides -- declares `virtual' packages for dependency purposes
    Description -- multiline description of package.
    Section -- application area of the package
        aircraft
        livery
        scenery
        plugin
        navdata
    Installed-Size -- installed size of the package (optional, calculated)
    Date -- last-modified-date of metadata
    Changes -- human-readable changelog data (optional)
    Size -- size of binary package (optional, calculated)
    MD5sum -- MD5 checksum of the package (optional, calculated)

  [source: PyPi additional key:value for installation]
    ReleaseURL -- The URL where to obtain the original ZIP package.


## Supporting Developers

To support Developers of X-Plane addons, it is aimed to provide a simple questionnaire to generate the metadata. The
metadate provided should be sufficient to download and install the .zip package into the X-Plane system without the
need to for extra information or other info files.