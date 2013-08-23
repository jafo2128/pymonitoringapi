# tests for dns_parser.py

import pytest
import sys
import os
import pkg_resources
import requests
import datetime

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/../../'))
from pymonitoringapi.APIs.nagios3 import Nagios3
from pymonitoringapi.exceptions import APItoServerMismatch

class TestAPIsNagios3:
    """
    Class to test APIs.Nagios3
    """

    def get_page_contents(self, url, method='get', req_params=None):
        """
        Mocked function to return a static file for a given URL request,
        to simulate a HTTP response. This doesn't return a mocked requests.response
        object, but rather just returns the "page content", like APIs.BaseAPI._get_page_content

        @param url string full URL to return

        returns a string of the page content
        """
        data_path = os.path.join(os.path.dirname(__file__), 'data', 'nagios3')

        # we lean on the requests package to get the full URL we'll request, with params
        r = requests.Request(method.upper(), url, auth=('foo', 'bar'), params=req_params).prepare()
        full_url = r.url
        page_name = full_url.split('/')[-1]

        page_file = os.path.join(data_path, page_name)

        print page_file
        if os.path.exists(page_file):
            try:
                with open(page_file, 'r') as fh:
                    data = fh.read()
                    return data
            except:
                return ""
        return ""

    @pytest.mark.parametrize(("host", "service", "ret_dict"), [
        ('localhost', 'nscatest', {'active_checks_enabled': False,
                                   'check_num': 1,
                                   'check_type': 0,
                                   'event_handler_enabled': True,
                                   'flap_detection_enabled': False,
                                   'flapping': False,
                                   'host': 'localhost',
                                   'is_in_downtime': False,
                                   'last_check_time': datetime.datetime(2013, 8, 21, 9, 16, 1),
                                   'max_num_checks': 1,
                                   'notifications_enabled': False,
                                   'obsessing_enabled': True,
                                   'output': 'CRITICAL: Passive check result is stale',
                                   'passive_checks_enabled': True,
                                   'service': 'nscatest',
                                   'state_type': 1,
                                   'status': 1})
    ])
    def test_parse_service_information(self, host, service, ret_dict):
        """
        Tests parsing the extinfo.cgi service status page HTML
        via APIs.Nagios3.get_service_information

        This uses get_page_contents static data files
        """
        Nagios3._get_page_content = self.get_page_contents
        api = Nagios3('http://nagios.example.com/nagios', 'username', 'password')
        svcinfo = api.get_service_information(host, service)
        assert svcinfo == ret_dict

    # @TODO - this should be a mock or monkeypatch?
    def page_return_empty_string(self, url, method='get', req_params=None):
        """
        return an empty string for a get_page_contents call
        """
        return ""

    def page_nagios_only(self, url, method='get', req_params=None):
        """
        return just the Nagios product div
        """
        return ' <div class="product">Nagios</div>'


    def test_non_matching_server(self):
        """
        Tests the Nagios3.__init__() exception raised when server doesn't match
        """
        Nagios3._get_page_content = self.page_return_empty_string
        with pytest.raises(APItoServerMismatch) as excinfo:
            api = Nagios3('http://nagios.example.com/nagios', 'username', 'password')
        assert excinfo.type == APItoServerMismatch

    def test_non_matching_version(self):
        """
        Tests the Nagios3.__init__() exception raised when server doesn't match,
        on a page that looks like Nagios but not Nagios3
        """
        Nagios3._get_page_content = self.page_nagios_only
        with pytest.raises(APItoServerMismatch) as excinfo:
            api = Nagios3('http://nagios.example.com/nagios', 'username', 'password')
        assert excinfo.type == APItoServerMismatch
