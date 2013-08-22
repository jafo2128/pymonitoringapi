"""
Nagios3 web-scraping client class.
"""

import requests
from baseapi import BaseAPI

class Nagios3(BaseAPI):
    """
    API (web scraping) client class for Nagios3.
    """

    system_name = "nagios"
    system_version = "3"

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
        Check the main page on the server, see if it's Nagios3.

        return True if we match, False otherwise.
        """
        content = self._get_page_content(self.base_url + "/main.php")
        print content


        """
@TODO - we should get back HTML page content that tells us the monitoring
system and version. i.e. we can look for substrings (or parse the HTML):

Nagios Core 3.3.1:

<div id="currentversioninfo">
<div class="product">Nagios<sup><span style="font-size: small;">&reg;</span></sup> Core<sup><span style="font-size: small;">&trade;</span></sup></div>
<div class="version">Version 3.3.1</div>
<div class="releasedate">July 25, 2011</div>
<div class="checkforupdates"><a href="http://www.nagios.org/checkforupdates/?version=3.3.1&product=nagioscore" target="_blank">Check for updates</a></div>
<!--<div class="whatsnew"><a href="http://go.nagios.com/nagioscore/whatsnew">Read what's new in Nagios Core 3</a></div>-->
</div>

Icinga 1.8.4:
<TITLE>Icinga</TITLE>

...

<div id="currentversioninfo">
<div class="version">Version 1.8.4</div>
<div class="releasedate">January 13, 2013</div>
<div class="whatsnew"><a href="docs/en/whatsnew.html">Read what's new in Icinga 1.8.4</a></div>
</div>

"""
