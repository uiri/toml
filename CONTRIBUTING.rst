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

There is a ``decoding_test.py`` script in the *tests/* directory
which acts as a harness in order to allow ``toml`` to be used with
the toml test suite, written (unfortunately) in Go.

Directions
----------

1. Install `Go <https://golang.org/>`_ (AKA golang)
2. Get the toml-test suite from `here <https://github.com/uiri/toml-test>`_
   and follow the instructions under the **Try it out** section of the README.
3. Test your changes for both versions of Python:

  * For Python 2, use ``~/go/bin/toml-test ./tests/decoding_test2.sh``
  * For Python 3, use ``~/go/bin/toml-test ./tests/decoding_test3.sh``
