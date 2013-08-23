This project is NOT working or ready for use yet!
=================================================

pymonitoringapi
=================

pymonitoringapi is a Python module to interact with and abstract the APIs of common
monitoring systems (currently targeted at Nagios and Icinga, but can be
expanded for anything with the same paradigms) the web. It is intended 
to handle most of the Web UI or API actions that would commonly be 
triggered from within a script, i.e. enable/disable notifications
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

Development
-----------

Issues/bugs are happily accepted on the tracker at https://github.com/jantman/pymonitoringapi/issues

Patches are happily accepted as Pull Requests on github. Before you submit a PR, please make sure:
* you've rebased against the latest version of the branch you're developing against (should currently be master)
* your new code (if any) has tests
* all tests pass
* coverage report (see below) is at least as good as when you started
* pep8 tests succeed

Testing
-------

Testing is currently done via py.test.

To get ready for testing:
```
pip install pytest pytest-cov pytest-cache pytest-pep8
```

To run the tests:
```
py.test
```

To run code coverage tests:
```
py.test --cov-report term-missing --cov=. tests/
```

To check pep8 compliance:
```
py.test --pep8
```


License
-------

pymonitoringapi is licensed under the [LGPL
v3](http://www.gnu.org/licenses/lgpl.html). You can view the text of the
license in the LICENSE file.

