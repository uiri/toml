#!/usr/bin/env python
"""Decodes toml and outputs it as JSON"""

import toml_test
import toml
import sys
import json

if __name__ == '__main__':
    tdata = toml.loads(sys.stdin.read())
    tagged = toml_test.tag(tdata)
    print(json.dumps(tagged))
