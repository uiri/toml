"""Decodes toml and outputs it as tagged JSON"""

import datetime
import json
import sys
import toml

if sys.version_info < (3,):
    _range = xrange  # noqa: F821
    iteritems = dict.iteritems
else:
    unicode = str
    _range = range
    basestring = str
    unichr = chr
    iteritems = dict.items
    long = int


def tag(value):
    if isinstance(value, dict):
        d = {}
        for k, v in iteritems(value):
            d[k] = tag(v)
        return d
    elif isinstance(value, list):
        a = []
        for v in value:
            a.append(tag(v))
        try:
            a[0]["value"]
        except KeyError:
            return a
        except IndexError:
            pass
        return {'type': 'array', 'value': a}
    elif isinstance(value, basestring):
        return {'type': 'string', 'value': value}
    elif isinstance(value, bool):
        return {'type': 'bool', 'value': str(value).lower()}
    elif isinstance(value, int):
        return {'type': 'integer', 'value': str(value)}
    elif isinstance(value, long):
        return {'type': 'integer', 'value': str(value)}
    elif isinstance(value, float):
        return {'type': 'float', 'value': repr(value)}
    elif isinstance(value, datetime.datetime):
        return {'type': 'datetime', 'value': value.isoformat()
                .replace('+00:00', 'Z')}
    elif isinstance(value, datetime.date):
        return {'type': 'date', 'value': value.isoformat()}
    elif isinstance(value, datetime.time):
        return {'type': 'time', 'value': value.strftime('%H:%M:%S.%f')}
    assert False, 'Unknown type: %s' % type(value)


if __name__ == '__main__':
    tdata = toml.loads(sys.stdin.read())
    tagged = tag(tdata)
    print(json.dumps(tagged))
