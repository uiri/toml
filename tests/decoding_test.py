#!/usr/bin/env python

"""Decodes TOML and outputs it as tagged JSON"""

import datetime
import json
import sys
import toml


def tag(value):
    if isinstance(value, dict):
        return {k: tag(v) for (k, v) in value.items()}
    elif isinstance(value, list):
        return [tag(v) for v in value]
    elif isinstance(value, str):
        return {'type': 'string', 'value': value}
    elif isinstance(value, bool):
        return {'type': 'bool', 'value': str(value).lower()}
    elif isinstance(value, int):
        return {'type': 'integer', 'value': str(value)}
    elif isinstance(value, float):
        return {'type': 'float', 'value': repr(value)}
    elif isinstance(value, datetime.datetime):
        return {
            'type': 'datetime-local' if value.tzinfo is None else 'datetime',
            'value': value.isoformat().replace('+00:00', 'Z'),
        }
    elif isinstance(value, datetime.date):
        return {'type': 'date-local', 'value': value.isoformat()}
    elif isinstance(value, datetime.time):
        return {'type': 'time-local', 'value': value.strftime('%H:%M:%S.%f')}
    assert False, 'Unknown type: %s' % type(value)


if __name__ == '__main__':
    tdata = toml.loads(sys.stdin.read())
    tagged = tag(tdata)
    print(json.dumps(tagged))
