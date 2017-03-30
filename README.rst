TOML
====

Original repository: https://github.com/uiri/toml

See also https://github.com/mojombo/toml

Python module which parses and emits TOML.

Released under the MIT license.

.. image:: https://badge.fury.io/py/toml.svg
    :target: https://badge.fury.io/py/toml

.. image:: https://travis-ci.org/uiri/toml.svg?branch=master
    :target: https://travis-ci.org/uiri/toml

Passes https://github.com/uiri/toml-test (fork of https://github.com/BurntSushi/toml-test )

Current Version of the Specification
------------------------------------

https://github.com/mojombo/toml/blob/v0.4.0/README.md

QUICK GUIDE
-----------

``pip install toml``

toml.loads --- takes a string to be parsed as toml and returns the corresponding dictionary

toml.dumps --- takes a dictionary and returns a string which is the contents of the corresponding toml file.

There are other functions which I use to dump and load various fragments of toml but dumps and loads will cover most usage.

API Reference
-------------

|

``toml.load(f, _dict=dict)`` - **Parses named file or files as toml and returns a dictionary**

:Args:
    f: Path to the file to open, array of files to read into single dict or a file descriptor
       
    _dict: (optional) Specifies the class of the returned toml dictionary

:Returns:
    Parsed toml file represented as a dictionary

:Raises:
    TypeError -- When array of non-strings is passed
    
    TypeError -- When f is invalid type
    
    TomlDecodeError: Error while decoding toml
    
|

``toml.loads(s, _dict=dict):`` - **Parses string as toml**

:Args:
    s: String to be parsed

    _dict: (optional) Specifies the class of the returned toml dictionary

:Returns:
    Parsed toml file represented as a dictionary

:Raises:
    TypeError: When a non-string is passed
    
    TomlDecodeError: Error while decoding toml
   
|

``toml.dump(o, f)`` **Writes out dict as toml to a file**

:Args:
    o: Object to dump into toml
    
    f: File descriptor where the toml should be stored

:Returns:
    String containing the toml corresponding to dictionary

:Raises:
    TypeError: When anything other than file descriptor is passed

|

``toml.dumps(o)`` **Stringifies input dict as toml**

:Args:
    o: Object to dump into toml

:Returns:
    String containing the toml corresponding to dict

Example usage
-------------

.. code:: python

  import toml

  with open("conf.toml") as conffile:
      config = toml.loads(conffile.read())
  # do stuff with config here
  . . .
