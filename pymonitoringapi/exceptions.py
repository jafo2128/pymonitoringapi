"""
All pymonitoringapi exceptions.

PasswordAuthException
HTTP404Exception
OtherHTTPException
NoApiClassFoundException
"""

class PasswordAuthException(Exception):
    """
    Exception raised when authentication to the API fails.

    Attributes:
        url      -- the URL that the error occurred on
        username -- the auth username that caused the error
        password -- the password used that caused the error
    """

    def __init__(self, url, username, password):
        self.url = url
        self.username = username
        self.password = password

    def __str__(self):
        return repr(self.url + " using credentials " + self.username + ":" + self.password)

class HTTP404Exception(Exception):
    """
    Exception raised when a URL returns a 404 status code.

    Attributes:
       url -- the URL that returned a HTTP 404 status code.
    """

    def __init__(self, url):
        self.url = url

    def __str__(self):
        return repr(self.url)

class OtherHTTPException(Exception):
    """
    Exception raised when a not-specifically-handled HTTP status code is received.

    Attributes:
        url  -- the URL that generated the status code
        code -- the HTTP status code
    """

    def __init__(self, url, code):
        self.url = url
        self.code = code

    def __str__(self):
        return repr(self.url, self.code)

class NoApiClassFoundException(Exception):
    """
    Exception raised when no appropriate API class can be found for a specific server.

    Attributes:
        url -- the base_url for the server
    """

    def __init__(self, base_url):
        self.base_url = base_url

    def __str__(self):
        return repr(self.base_url)

class APItoServerMismatch(Exception):
    """
    Exception raised when an API class doesn't match the
    server we are connecting to.

    Attributes:
        url       -- the base_url to the server
        classname -- the name of the class
    """

    def __init__(self, url, classname):
        self.url = url
        self.classname = classname

    def __str__(self):
        return repr(self.url + self.classname)
