"""
TODO: something
"""

import requests

__version__ = '0.0.1'

"""
NagiosAPI is the main class instantiated by applications.

It handles connection to the Nagios/Icinga/etc. instance, detection
of the server type and version, and returning the appropriate object.

"""
class NagiosAPI:

    def get_main_page(self):
        """
        Attempt a HTTP request to the main URL specified.
        Return the page content, or raise an exception.
        """
        # page URLs to try - we want to get as much information as
        # we can, so we go from specific to general
        try_pages = ['/foobar', '/main.php', '/']
        for page in try_pages:
            res = requests.get(self.base_url + page, auth=(self.username, self.password))
            if res.ok:
                if res.status_code == 200:
                    return res.content
                else:
                    # @todo - handle or raise exception?
                    pass
            else:
                # @todo - handle or raise exception?
                pass
        # @todo should never get here
        return None

    def __init__(self, base_url, username, password, cgipath='cgi-bin/'):
        """
        Initialize NagiosAPI. Try a HTTP request to the server, verify
        credentials. Assuming the request works, dynamically load all classes
        under APIs/ and attempt to identify the correct one to communicate 
        with our server. Return an instance of it.

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

        page_content = self.get_main_page()
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
        print page_content
        # move ALL of the above stuff to each class under APIs/
        # we need to dynamically load each of the classes under APIs/, 
        # and run their _matches_current_server() methods, waiting
        # for one of them to return True. 
        # if none of them do, we raise an Exception.
