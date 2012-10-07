# borrowed some functions from the pip project. (http://www.pip-installer.org)
# that code is written under the MIT license, copyright by the pip-developers

import posixpath
import re
import urlparse
from util import Inf
from util import splitext

class Link(object):

    def __init__(self, url, comes_from=None):
        self.url = url
        self.comes_from = comes_from

    def __str__(self):
        if self.comes_from:
            return '%s (from %s)' % (self.url, self.comes_from)
        else:
            return str(self.url)

    def __repr__(self):
        return '<Link %s>' % self

    def __eq__(self, other):
        return self.url == other.url

    def __ne__(self, other):
        return self.url != other.url

    def __lt__(self, other):
        return self.url < other.url

    def __le__(self, other):
        return self.url <= other.url

    def __gt__(self, other):
        return self.url > other.url

    def __ge__(self, other):
        return self.url >= other.url

    def __hash__(self):
        return hash(self.url)

    @property
    def filename(self):
        _, netloc, path, _, _ = urlparse.urlsplit(self.url)
        name = posixpath.basename(path.rstrip('/')) or netloc
        assert name, ('URL %r produced no filename' % self.url)
        return name

    @property
    def scheme(self):
        return urlparse.urlsplit(self.url)[0]

    @property
    def path(self):
        return urlparse.urlsplit(self.url)[2]

    def splitext(self):
        return splitext(posixpath.basename(self.path.rstrip('/')))

    @property
    def url_without_fragment(self):
        scheme, netloc, path, query, fragment = urlparse.urlsplit(self.url)
        return urlparse.urlunsplit((scheme, netloc, path, query, None))

    _egg_fragment_re = re.compile(r'#egg=([^&]*)')

    @property
    def egg_fragment(self):
        match = self._egg_fragment_re.search(self.url)
        if not match:
            return None
        return match.group(1)

    _hash_re = re.compile(r'(sha1|sha224|sha384|sha256|sha512|md5)=([a-f0-9]+)')

    @property
    def hash(self):
        match = self._hash_re.search(self.url)
        if match:
            return match.group(2)
        return None

    @property
    def hash_name(self):
        match = self._hash_re.search(self.url)
        if match:
            return match.group(1)
        return None

    @property
    def show_url(self):
        return posixpath.basename(self.url.split('#', 1)[0].split('?', 1)[0])

#An "Infinite Link" that compares greater than other links
InfLink = Link(Inf)
