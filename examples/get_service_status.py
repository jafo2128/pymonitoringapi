#!/usr/bin/env python

"""
pymonitoringapi example script to find the server type
and version of our monitoring server.
"""

import optparse
import sys
import os
import pprint

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../")))

from pymonitoringapi import MonitoringAPI

VERBOSE = False

def show_service_status(host, service, user, password, url, cgibin):
    mon = MonitoringAPI(url, user, password, cgibin)
    client = mon.get_client()

    status = client.get_service_information(host, service)
    pprint.pprint(status)

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

    parser.add_option('-H', '--host', dest='host',
                      help='hostname to check status for')

    parser.add_option('-s', '--service', dest='service',
                      help='(optional) service to check status for')

    options, args = parser.parse_args()

    if not options.user or not options.password or not options.url:
        print "ERROR: you must specify -u/--user, -p/--password and -U/--url"
        sys.exit(1)

    if options.verbose:
        VERBOSE = True

    if not options.host:
        print "ERROR: you must specify -h/--host to check status for"
        sys.exit(1)

    if not options.service:
        print "host status not implemented yet"
    else:
        show_service_status(options.host, options.service, options.user, options.password, options.url, options.cgibin)
