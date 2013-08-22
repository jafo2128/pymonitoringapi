"""
Nagios3 web-scraping client class.
"""

import requests
from baseapi import BaseAPI
import re

class Nagios3(BaseAPI):
    """
    API (web scraping) client class for Nagios3.
    """

    system_name = "nagios"
    system_major_version = 3 # this class only supports Nagios3
    system_full_version = None
    classname = __name__

    def __init__(self, base_url, username, password, cgipath='cgi-bin/'):
        """
        Initialize, set class variables, try a HTTP login, and check
        that this is the correct class for this server.

        @param base_url string the URL to our Nagios installation (i.e. http://host.example.com/nagios/).
        @param username string the username to authenticate with (HTTP Basic Auth).
        @param password string the password to authenticate with (HTTP Basic Auth).
        @param cgipath string the path (appended to base_url) to get to our installation's
          cgi-bin directory. Default is "nagios/cgi-bin/"
        """
        self.base_url = base_url
        self.username = username
        self.password = password
        self.cgipath = cgipath
        match = self._is_matching_server()
        if not match:
            raise APItoServerMismatch(base_url, __name__)

    def _is_matching_server(self):
        """
        Check the main page on the server, see if it's Nagios3 (and therefore supported by this class).

        return True if we match, False otherwise.
        """
        content = self._get_page_content(self.base_url + "/main.php")

        # we could use BeautifulSoup, but it's not really worth it here...
        if re.search(r'<div class="product">Nagios', content):
            # yup, it's nagios
            foo = re.search('<div class="version">Version (3\.(\d\.\d))</div>', content)
            if foo:
                self.system_full_version = foo.groups(0)[0]
                return True
            else:
                return False
        return False
