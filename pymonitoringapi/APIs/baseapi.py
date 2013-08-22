"""
Base class for all monitoring system clients (Nagios/Icinga/etc.) API classes.
"""

import requests
from pymonitoringapi.exceptions import *
from pymonitoringapi import constants

class BaseAPI:
    """
    Base class for all monitoring system clients (Nagios/Icinga/etc.) API classes.
    """

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

    def _is_matching_server(self):
        """
        Return True if the server at the specified base_url matches
        what this class handles, False otherwise.

        This should be overridden by the inheriting class.
        """
        return False

    def get_major_version(self):
        """
        Return the major version of the monitoring server.

        return integer, major version of monitoring system.
        """
        return self.system_major_version

    def get_full_version(self):
        """
        Return the full version of the monitoring server.

        return string, full version of monitoring system.
        """
        return self.system_full_version

    def get_system_name(self):
        """
        Return the name of the monitoring system that this class supports.

        return string, name of supported monitoring system
        """
        return self.system_name

    def _get_page_content(self, url, method='get', req_params=None):
        """
        Gets the content of a url over HTTP.

        @param url string the URL to get
        @param method "get" or "post", method to use, default 'get'
        @param dict req_params request parameters

        Raises:
            PasswordAuthException -- when we get a HTTP 401
            HTTP404Exception      -- when we get a HTTP 404
            OtherHTTPException    -- when we get another non-200 HTTP code
        """
        if method == "get":
            res = requests.get(url, auth=(self.username, self.password), params=req_params)
        elif method == "post":
            res = requests.post(url, auth=(self.username, self.password), params=req_params)
        else:
            print "not implemented" # TODO fix this
            return None
        if res.status_code == 200:
            return res.content
        if res.status_code == 401:
            raise PasswordAuthException(url, self.username, self.password)
        elif res.status_code == 404:
            raise HTTP404Exception(url)
        else:
            raise OtherHTTPException(url, res.status_code)
        # we should NEVER get here
        return None
