************
Contributing
************

Issues and Pull Requests are always welcome. Thank you in advance for
your contribution!

Reporting Issues
================

Before reporting an issue, please test the issue using the latest
development version to see if your issue has been fixed since the
latest release.

Testing
=======

### Unit tests
Unit tests can be run using [tox](https://tox.readthedocs.io/en/latest/).
Simply `pip install tox` and you are ready to go. Tox creates required
virual eniroments and installs necessary packages.

    tox

This is not very practical for day to day use. To easily run tests
in the current Python simply run.

    tox -e py

We are using [pytest](https://docs.pytest.org/en/latest/) testing framework.
You can pass parameters to it like this:

    tox -e py -- -vsx


### Decoding tests
There is a ``decoding_test.py`` script in the *tests/* directory
which acts as a harness in order to allow ``toml`` to be used with
the toml test suite, written (unfortunately) in Go.

Directions
----------

1. Install `Go <https://golang.org/>`_ (AKA golang)
2. Get the toml-test suite from `here <https://github.com/BurntSushi/toml-test>`_
   and follow the instructions under the **Try it out** section of the README.
3. Test your changes for both versions of Python:

  * For Python 2, use ``~/go/bin/toml-test ./tests/decoding_test2.sh``
  * For Python 3, use ``~/go/bin/toml-test ./tests/decoding_test3.sh``
