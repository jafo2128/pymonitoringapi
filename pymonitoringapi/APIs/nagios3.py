"""
Nagios3 web-scraping client class.
"""

import requests
from baseapi import BaseAPI
import re
from bs4 import BeautifulSoup
from pymonitoringapi import constants
from datetime import datetime
from pymonitoringapi.exceptions import *

class Nagios3(BaseAPI):
    """
    API (web scraping) client class for Nagios3.
    """

    system_name = "nagios"
    system_major_version = 3 # this class only supports Nagios3
    system_full_version = None
    classname = __name__

    time_format = '%m-%d-%Y %H:%M:%S'

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

    def get_service_information(self, hostname, servicename):
        """
        Gets all state information relating to a given service.

        returns a dict with, at a minimum, the following keys
            host -- string, name of the host this service is on
            service -- string, name of the service
            status -- int, current status of the service, see constants.STATUS_*

        the following values will NOT be present if status is STATUS_PENDING
            output -- string, output from the check/plugin/whatever, textual description of status
            flapping -- boolean, whether or not the service is flapping (True if flapping)
            check_type -- int, type of check (active or passive), see constants.CHECK_TYPE_*
            last_check_time -- DateTime, when the last check occurred or came in
            is_in_downtime -- boolean, True if host is currently in scheduled downtime
            max_num_checks -- maximum number of checks before service goes to a HARD state
            check_num -- current check number out of max_num_checks
            obsessing_enabled -- boolean, True if obsessing is enabled for this service
            passive_checks_enabled -- boolean, True if passive checks are enabled
            active_checks_enabled -- boolean, True if active checks are enabled
            notifications_enabled -- boolean, True if notifications are enabled
            event_handler_enabled -- boolean, True if event handler is enabled
            flap_detection_enabled -- boolean, True if flap detection is enabled
        """
        params = {
            'type': 2,
            'host': hostname,
            'service': servicename,
            }
        content = self._get_page_content(self.base_url + self.cgipath + "/extinfo.cgi", req_params=params)

        if 'It appears as though you do not have permission to view information for this service...' in content:
            raise PermissionsException("service %s on host %s" % (servicename, hostname))

        if 'This service has not yet been checked, so status information is not available.' in content:
            # hasn't been checked yet, NO information
            return {'status': constants.STATUS_PENDING, 'host': hostname, 'service': servicename}

        ret = {'status': constants.STATUS_UNDETERMINED, 'host': hostname, 'service': servicename}

        soup = BeautifulSoup(content)

        status = str(soup.find('td', text='Current Status:').findParent('tr').find('td', attrs={'class': 'dataVal'}).find('div').attrs['class'][0])
        if status == 'serviceOK':
            ret['status'] = constants.STATUS_OK
        elif status == 'serviceCRITICAL':
            ret['status'] = constants.STATUS_CRITICAL
        elif status == 'serviceWARNING':
            ret['status'] = constants.STATUS_WARNING
        elif status == 'serviceUNKNOWN':
            ret['status'] = constants.STATUS_UNKNOWN
        else:
            ret['status'] = constants.STATUS_UNDETERMINED

        ret['output'] = str(soup.find('td', text='Status Information:').findParent('tr').find('td', attrs={'class': 'dataVal'}).string)

        # @TODO: perfdata

        foo = soup.find('td', text='Current Attempt:').findParent('tr').find('td', attrs={'class': 'dataVal'}).string
        foo = re.search('(\d)/(\d).+\((\w+) state\)', foo)
        if foo:
            ret['check_num'] = int(foo.group(1))
            ret['max_num_checks'] = int(foo.group(2))
            if foo.group(3) == "HARD":
                ret['state_type'] = constants.STATE_HARD
            elif foo.group(3) == "SOFT":
                ret['state_type'] = constants.STATE_SOFT
            else:
                ret['state_type'] = constants.STATE_UNKNOWN

        last_check_time = str(soup.find('td', text='Last Check Time:').findParent('tr').find('td', attrs={'class': 'dataVal'}).string)
        ret['last_check_time'] = datetime.strptime(last_check_time, self.time_format)

        check_type = soup.find('td', text='Check Type:').findParent('tr').find('td', attrs={'class': 'dataVal'}).string
        if check_type == "ACTIVE":
            ret['check_type'] = constants.CHECK_TYPE_ACTIVE
        elif check_type == "PASSIVE":
            ret['check_type'] = constants.CHECK_TYPE_PASSIVE

        downtime = str(soup.find('td', text='In Scheduled Downtime?').findParent('tr').find('td', attrs={'class': 'dataVal'}).find('div').attrs['class'][0])
        if downtime == 'downtimeINACTIVE':
            ret['is_in_downtime'] = False
        else:
            ret['is_in_downtime'] = True

        active_checks = str(soup.find('td', text='Active Checks:').findParent('tr').find('td', attrs={'class': 'dataVal'}).find('div').attrs['class'][0])
        if active_checks == 'checksDISABLED':
            ret['active_checks_enabled'] = False
        else:
            ret['active_checks_enabled'] = True

        passive_checks = str(soup.find('td', text='Passive Checks:').findParent('tr').find('td', attrs={'class': 'dataVal'}).find('div').attrs['class'][0])
        if passive_checks == 'checksDISABLED':
            ret['passive_checks_enabled'] = False
        else:
            ret['passive_checks_enabled'] = True

        obsessing = str(soup.find('td', text='Obsessing:').findParent('tr').find('td', attrs={'class': 'dataVal'}).find('div').attrs['class'][0])
        if obsessing == 'checksDISABLED':
            ret['obsessing_enabled'] = False
        else:
            ret['obsessing_enabled'] = True

        notifications = str(soup.find('td', text='Notifications:').findParent('tr').find('td', attrs={'class': 'dataVal'}).find('div').attrs['class'][0])
        if notifications == 'notificationsDISABLED':
            ret['notifications_enabled'] = False
        else:
            ret['notifications_enabled'] = True

        event_handler = str(soup.find('td', text='Event Handler:').findParent('tr').find('td', attrs={'class': 'dataVal'}).find('div').attrs['class'][0])
        if event_handler == 'eventhandlerDISABLED':
            ret['event_handler_enabled'] = False
        else:
            ret['event_handler_enabled'] = True

        flap_detection = str(soup.find('td', text='Flap Detection:').findParent('tr').find('td', attrs={'class': 'dataVal'}).find('div').attrs['class'][0])
        if flap_detection == 'flapdetectionDISABLED':
            ret['flap_detection_enabled'] = False
            ret['flapping'] = False
        else:
            ret['flap_detection_enabled'] = True
            flapping = soup.find('td', text='Is This Service Flapping?').findParent('tr').find('div').attrs['class'][0]
            if flapping == "notflapping":
                ret['flapping'] = False
            else:
                ret['flapping'] = True


        return ret


"""
Stuff we still need to parse from the html

<TR><TD CLASS='dataVar' NOWRAP>Check Latency / Duration:</TD><TD CLASS='dataVal'>1.091&nbsp;/&nbsp;0.025 seconds</TD></TR>
<TR><TD CLASS='dataVar'>Next Scheduled Check:&nbsp;&nbsp;</TD><TD CLASS='dataVal'>N/A</TD></TR>
<TR><TD CLASS='dataVar'>Last State Change:</TD><TD CLASS='dataVal'>08-21-2013 09:16:01</TD></TR>
<TR><TD CLASS='dataVar'>Last Notification:</TD><TD CLASS='dataVal'>N/A&nbsp;(notification 0)</TD></TR>
<TR><TD CLASS='dataVar'>Last Update:</TD><TD CLASS='dataVal'>08-22-2013 10:35:52&nbsp;&nbsp;( 0d  0h  0m  8s ago)</TD></TR>

"""
