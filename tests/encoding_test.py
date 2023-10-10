#!/usr/bin/env python

"""Reads tagged JSON and encodes it as TOML"""

import json
import sys
import toml

def convert(v):
    if type(v) == list:
        return [convert(vv) for vv in v]
    elif v.get('type', None) is None or v.get('value', None) is None:
        return {k: convert(vv) for (k, vv) in v.items()}
    elif v['type'] == 'string':
        return v['value']
    elif v['type'] == 'integer':
        return int(v['value'])
    elif v['type'] == 'float':
        return float(v['value'])
    elif v['type'] == 'bool':
        return True if v['value'] == 'true' else False
    elif v['type'] in ['datetime', 'datetime-local', 'date-local', 'time-local']:
        return toml.loads('a=' + v['value'])['a']
    else:
        raise Exception(f'unknown type: {v}')

j = json.loads(sys.stdin.read())
print(toml.dumps({k: convert(v) for (k, v) in j.items()}))
