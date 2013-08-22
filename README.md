pynagiosapi
=================

pynagiosapi is a Python module to interact with Nagios and Icinga over
the web. It is intended to handle most of the Web UI actions that would
commonly be triggered from within a script, i.e. enable/disable notifications
or checks, schedule and delete downtime, check host or service status, etc.

For Nagios, this module uses BeautifulSoup to parse the HTML of the web
interface, since Nagios doesn't have a real API. For Icinga, we use the REST
API.

This module was inspired by Alexandr Skurikhin's
[nagiosharder](https://pypi.python.org/pypi/nagiosharder/0.1.1) module, which
in turn is a port of railsmachine's [nagiosharder ruby gem](https://github.com/railsmachine/nagiosharder).

Current State
-------------

- Icinga support: not even started
- Nagios support:
  - initial plan is to support downtimes only, for now.

Installation
------------

    Hopefully this will end up on pypi once it's mostly working.

Usage
-----

    import foo

Examples
--------

    Something will go here...

License
-------

python-nagios-api is licensed under the [LGPL
v3](http://www.gnu.org/licenses/lgpl.html). You can view the text of the
license in the LICENSE file.

