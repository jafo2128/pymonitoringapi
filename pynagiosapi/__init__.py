"""
NagiosAPI class.
"""

import requests
from exceptions import *

__version__ = '0.0.1'

class NagiosAPI:
    """
    NagiosAPI is the main class instantiated by applications.

    It handles connection to the Nagios/Icinga/etc. instance, detection
    of the server type and version, and returning the appropriate object.
    """

    """
    The working APIs/ classes should be listed here, by class name.
    When a new NagiosAPI object is instantiated and the api_class
    parameter isn't provided, we'll try instantiating each of these
    classes in order, until we find one that works.
    """
    API_CLASSES = ['Nagios3']

    client = None

    def __init__(self, base_url, username, password, cgipath='cgi-bin/', api_class=None):
        """
        Initialize NagiosAPI. Try to instantiate each of the APIs/ classes
        (listed in self.API_CLASSES) and get one that "claims" the specified
        server. Else, raise an exception.

        @param base_url string the URL to our Nagios installation (i.e. http://host.example.com/nagios/).
        @param username string the username to authenticate with (HTTP Basic Auth).
        @param password string the password to authenticate with (HTTP Basic Auth).
        @param cgipath string the path (appended to base_url) to get to our installation's
          cgi-bin directory. Default is "nagios/cgi-bin/"
        @param api_class string (optional) the name of the API class to use for this server.
        If not specified, will test each available class at object creation time until a
        match is found. See pynagiosapi/__init__.py for available options.
        """

        # if we were called with api_class, only try that API class
        if api_class is not None:
            self.API_CLASSES = [api_class]

        # iterate through the API classes, try importing and instantiating them
        for modname in self.API_CLASSES:
            # try to import the module
            try:
                mod = __import__("pynagiosapi.APIs." + modname.lower(), fromlist=[modname])
                client_class = getattr(mod, modname)
            except:
                print "Couldn't import module %s" % modname # DEBUG LOG
                continue
            # instantiate it, see what it does...
            try:
                client = client_class(base_url, username, password, cgipath)
                self.client = client
            except PasswordAuthException as e:
                print e
                continue

        if self.client is None:
            raise NoApiClassFoundException(base_url)

        # move ALL of the above stuff to each class under APIs/
        # we need to dynamically load each of the classes under APIs/, 
        # and run their _matches_current_server() methods, waiting
        # for one of them to return True. 
        # if none of them do, we raise an Exception.
