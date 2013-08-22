#!/usr/bin/env python

"""
pymonitoringapi example script to find the server type
and version of our monitoring server.
"""

import optparse
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../")))

from pymonitoringapi import MonitoringAPI

VERBOSE = False

def show_server_ver(user, password, url, cgibin):
    client = MonitoringAPI(url, user, password, cgibin)
    print client

if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option('-u', '--user', dest='user',
                      help='username to authenticate with (HTTP Basic Auth)')

    parser.add_option('-p', '--password', dest='password',
                      help='password to authenticate with (HTTP Basic Auth)')

    parser.add_option('-U', '--url', dest='url',
                      help='url to the top-level nagios web directory (i.e. http://host.example.com/nagios/)')

    parser.add_option('-c', '--cgibin', dest='cgibin', default='cgi-bin/',
                      help='path to nagios cgi-bin directory, relative to url (default: cgi-bin/)')

    parser.add_option('-v', '--verbose', dest='verbose', default=False, action='store_true',
                      help='verbose (debug-level) output')

    options, args = parser.parse_args()

    if not options.user or not options.password or not options.url:
        print "ERROR: you must specify -u/--user, -p/--password and -U/--url"
        sys.exit(1)

    if options.verbose:
        VERBOSE = True

    show_server_ver(options.user, options.password, options.url, options.cgibin)
