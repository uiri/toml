#!/usr/bin/env python3

import toml_test
import toml
import sys
import json

if __name__ == '__main__':
    tdata = toml.loads(sys.stdin.detach().read().decode('utf-8'))
    tagged = toml_test.tag(tdata)
    print(json.dumps(tagged))
