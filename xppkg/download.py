# borrowed some functions from the pip project. (http://www.pip-installer.org)
# that code is written under the MIT license, copyright by the pip-developers

"""
download.py contains functions to download files
"""
import cgi
import getpass
import hashlib
import mimetypes
import os
import re
import shutil
import tempfile
import urllib
import urllib2
import urlparse
import sys
from xppkg.backwardcompat import string_types
from xppkg.exceptions import InstallationError
from xppkg.util import create_download_cache_folder, splitext, format_size, display_path, backup_dir, ask_path_exists, unpack_file, cache_download
from xppkg.log import logger

_url_re = re.compile(r'^(http|https):', re.I)

def unpack_http_url(link, location, download_cache=None, download_dir=None):
    """
    downloads and unpacks a archive to a directory

    link is a  index.Link object (with an url)
    location is ...
    download_cache is the dir where the download cache is stored
    download_dir is optional a dir where the download is first stored
    """
    temp_dir = tempfile.mkdtemp('-unpack', 'xppkg-')
    target_url = link.url.split('#', 1)[0]
    target_file = None
    download_hash = None
    if download_cache:
        target_file = os.path.join(download_cache,
            urllib.quote(target_url, ''))
        if not os.path.isdir(download_cache):
            create_download_cache_folder(download_cache)

    already_downloaded = None
    if download_dir:
        already_downloaded = os.path.join(download_dir, link.filename)
        if not os.path.exists(already_downloaded):
            already_downloaded = None

    if (target_file
        and os.path.exists(target_file)
        and os.path.exists(target_file + '.content-type')):
        fp = open(target_file+'.content-type')
        content_type = fp.read().strip()
        fp.close()
        if link.hash and link.hash_name:
            download_hash = _get_hash_from_file(target_file, link)
        temp_location = target_file
        logger.notify('Using download cache from %s' % target_file)
    elif already_downloaded:
        temp_location = already_downloaded
        content_type = mimetypes.guess_type(already_downloaded)
        if link.hash:
            download_hash = _get_hash_from_file(temp_location, link)
        logger.notify('File was already downloaded %s' % already_downloaded)
    else:
        resp = _get_response_from_url(target_url, link)
        content_type = resp.info()['content-type']
        filename = link.filename  # fallback
        # Have a look at the Content-Disposition header for a better guess
        content_disposition = resp.info().get('content-disposition')
        if content_disposition:
            type, params = cgi.parse_header(content_disposition)
            # We use ``or`` here because we don't want to use an "empty" value
            # from the filename param.
            filename = params.get('filename') or filename
        ext = splitext(filename)[1]
        if not ext:
            ext = mimetypes.guess_extension(content_type)
            if ext:
                filename += ext
        if not ext and link.url != geturl(resp):
            ext = os.path.splitext(geturl(resp))[1]
            if ext:
                filename += ext
        temp_location = os.path.join(temp_dir, filename)
        download_hash = _download_url(resp, link, temp_location)
    if link.hash and link.hash_name:
        _check_hash(download_hash, link)
    if download_dir and not already_downloaded:
        _copy_file(temp_location, download_dir, content_type, link)
    unpack_file(temp_location, location, content_type, link)
    if target_file and target_file != temp_location:
        cache_download(target_file, temp_location, content_type)
    if target_file is None and not already_downloaded:
        os.unlink(temp_location)
    os.rmdir(temp_dir)


def geturl(urllib2_resp):
    """
    Use instead of urllib.addinfourl.geturl(), which appears to have
    some issues with dropping the double slash for certain schemes
    (e.g. file://).  This implementation is probably over-eager, as it
    always restores '://' if it is missing, and it appears some url
    schemata aren't always followed by '//' after the colon, but as
    far as I know pip doesn't need any of those.
    The URI RFC can be found at: http://tools.ietf.org/html/rfc1630

    This function assumes that
        scheme:/foo/bar
    is the same as
        scheme:///foo/bar
    """
    url = urllib2_resp.geturl()
    scheme, rest = url.split(':', 1)
    if rest.startswith('//'):
        return url
    else:
        # FIXME: write a good test to cover it
        return '%s://%s' % (scheme, rest)

def _get_hash_from_file(target_file, link):
    try:
        download_hash = hashlib.new(link.hash_name)
    except (ValueError, TypeError):
        logger.warn("Unsupported hash name %s for package %s" % (link.hash_name, link))
        return None

    fp = open(target_file, 'rb')
    while True:
        chunk = fp.read(4096)
        if not chunk:
            break
        download_hash.update(chunk)
    fp.close()
    return download_hash

def download_url(url):
    """
    Downloads an URL to a directory

    returns content of the url

    :type url: str
    """
    assert _url_re.search(url)
    returns = urlopen(url).read()

def is_archive_file(name):
    """Return True if `name` is a considered as an archive file."""
    archives = ('.zip', '.tar.gz', '.tar.bz2', '.tgz', '.tar', '.pybundle')
    ext = splitext(name)[1].lower()
    if ext in archives:
        return True
    return False

class URLOpener(object):
    """
    pip's own URL helper that adds HTTP auth and proxy support
    """
    def __init__(self):
        self.passman = urllib2.HTTPPasswordMgrWithDefaultRealm()

    def __call__(self, url):
        """
        If the given url contains auth info or if a normal request gets a 401
        response, an attempt is made to fetch the resource using basic HTTP
        auth.

        """
        url, username, password = self.extract_credentials(url)
        if username is None:
            try:
                response = urllib2.urlopen(self.get_request(url))
            except urllib2.HTTPError:
                e = sys.exc_info()[1]
                if e.code != 401:
                    raise
                response = self.get_response(url)
        else:
            response = self.get_response(url, username, password)
        return response

    def get_request(self, url):
        """
        Wraps the URL to retrieve to protects against "creative"
        interpretation of the RFC: http://bugs.python.org/issue8732
        """
        if isinstance(url, string_types):
            url = urllib2.Request(url, headers={'Accept-encoding': 'identity'})
        return url

    def get_response(self, url, username=None, password=None):
        """
        does the dirty work of actually getting the rsponse object using urllib2
        and its HTTP auth builtins.
        """
        scheme, netloc, path, query, frag = urlparse.urlsplit(url)
        req = self.get_request(url)

        stored_username, stored_password = self.passman.find_user_password(None, netloc)
        # see if we have a password stored
        if stored_username is None:
            if username is None and self.prompting:
                username = urllib.quote(raw_input('User for %s: ' % netloc))
                password = urllib.quote(getpass.getpass('Password: '))
            if username and password:
                self.passman.add_password(None, netloc, username, password)
            stored_username, stored_password = self.passman.find_user_password(None, netloc)
        authhandler = urllib2.HTTPBasicAuthHandler(self.passman)
        opener = urllib2.build_opener(authhandler)
        # FIXME: should catch a 401 and offer to let the user reenter credentials
        return opener.open(req)

    def setup(self, proxystr='', prompting=True):
        """
        Sets the proxy handler given the option passed on the command
        line.  If an empty string is passed it looks at the HTTP_PROXY
        environment variable.
        """
        self.prompting = prompting
        proxy = self.get_proxy(proxystr)
        if proxy:
            proxy_support = urllib2.ProxyHandler({"http": proxy, "ftp": proxy, "https": proxy})
            opener = urllib2.build_opener(proxy_support, urllib2.CacheFTPHandler)
            urllib2.install_opener(opener)

    def parse_credentials(self, netloc):
        if "@" in netloc:
            userinfo = netloc.rsplit("@", 1)[0]
            if ":" in userinfo:
                return userinfo.split(":", 1)
            return userinfo, None
        return None, None

    def extract_credentials(self, url):
        """
        Extracts user/password from a url.

        Returns a tuple:
            (url-without-auth, username, password)
        """
        if isinstance(url, urllib2.Request):
            result = urlparse.urlsplit(url.get_full_url())
        else:
            result = urlparse.urlsplit(url)
        scheme, netloc, path, query, frag = result

        username, password = self.parse_credentials(netloc)
        if username is None:
            return url, None, None
        elif password is None and self.prompting:
            # remove the auth credentials from the url part
            netloc = netloc.replace('%s@' % username, '', 1)
            # prompt for the password
            prompt = 'Password for %s@%s: ' % (username, netloc)
            password = urllib.quote(getpass.getpass(prompt))
        else:
            # remove the auth credentials from the url part
            netloc = netloc.replace('%s:%s@' % (username, password), '', 1)

        target_url = urlparse.urlunsplit((scheme, netloc, path, query, frag))
        return target_url, username, password

    def get_proxy(self, proxystr=''):
        """
        Get the proxy given the option passed on the command line.
        If an empty string is passed it looks at the HTTP_PROXY
        environment variable.
        """
        if not proxystr:
            proxystr = os.environ.get('HTTP_PROXY', '')
        if proxystr:
            if '@' in proxystr:
                user_password, server_port = proxystr.split('@', 1)
                if ':' in user_password:
                    user, password = user_password.split(':', 1)
                else:
                    user = user_password
                    prompt = 'Password for %s@%s: ' % (user, server_port)
                    password = urllib.quote(getpass.getpass(prompt))
                return '%s:%s@%s' % (user, password, server_port)
            else:
                return proxystr
        else:
            return None

urlopen = URLOpener()

def _copy_file(filename, location, content_type, link):
    copy = True
    download_location = os.path.join(location, link.filename)
    if os.path.exists(download_location):
        response = ask_path_exists(
            'The file %s exists. (i)gnore, (w)ipe, (b)ackup ' %
            display_path(download_location), ('i', 'w', 'b'))
        if response == 'i':
            copy = False
        elif response == 'w':
            logger.warn('Deleting %s' % display_path(download_location))
            os.remove(download_location)
        elif response == 'b':
            dest_file = backup_dir(download_location)
            logger.warn('Backing up %s to %s'
                        % (display_path(download_location), display_path(dest_file)))
            shutil.move(download_location, dest_file)
    if copy:
        shutil.copy(filename, download_location)
        logger.indent -= 2
        logger.notify('Saved %s' % display_path(download_location))

def _get_response_from_url(target_url, link):
    try:
        resp = urlopen(target_url)
    except urllib2.HTTPError:
        e = sys.exc_info()[1]
        logger.fatal("HTTP error %s while getting %s" % (e.code, link))
        raise
    except IOError:
        e = sys.exc_info()[1]
        # Typically an FTP error
        logger.fatal("Error %s while getting %s" % (e, link))
        raise
    return resp

def _check_hash(download_hash, link):
    if download_hash.digest_size != hashlib.new(link.hash_name).digest_size:
        logger.fatal("Hash digest size of the package %d (%s) doesn't match the expected hash name %s!"
                     % (download_hash.digest_size, link, link.hash_name))
        raise InstallationError('Hash name mismatch for package %s' % link)
    if download_hash.hexdigest() != link.hash:
        logger.fatal("Hash of the package %s (%s) doesn't match the expected hash %s!"
                     % (link, download_hash, link.hash))
        raise InstallationError('Bad %s hash for package %s' % (link.hash_name, link))

def _download_url(resp, link, temp_location):
    fp = open(temp_location, 'wb')
    download_hash = None
    if link.hash and link.hash_name:
        try:
            download_hash = hashlib.new(link.hash_name)
        except ValueError:
            logger.warn("Unsupported hash name %s for package %s" % (link.hash_name, link))
    try:
        total_length = int(resp.info()['content-length'])
    except (ValueError, KeyError, TypeError):
        total_length = 0
    downloaded = 0
    show_progress = total_length > 40*1000 or not total_length
    show_url = link.show_url
    try:
        if show_progress:
            ## FIXME: the URL can get really long in this message:
            if total_length:
                logger.start_progress('Downloading %s (%s): ' % (show_url, format_size(total_length)))
            else:
                logger.start_progress('Downloading %s (unknown size): ' % show_url)
        else:
            logger.notify('Downloading %s' % show_url)
        logger.info('Downloading from URL %s' % link)

        while True:
            chunk = resp.read(4096)
            if not chunk:
                break
            downloaded += len(chunk)
            if show_progress:
                if not total_length:
                    logger.show_progress('%s' % format_size(downloaded))
                else:
                    logger.show_progress('%3i%%  %s' % (100*downloaded/total_length, format_size(downloaded)))
            if download_hash is not None:
                download_hash.update(chunk)
            fp.write(chunk)
        fp.close()
    finally:
        if show_progress:
            logger.end_progress('%s downloaded' % format_size(downloaded))
    return download_hash
