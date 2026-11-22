try:
    from collections import UserDict
except ImportError:
    from UserDict import UserDict

import toml


def test_userdict_roundtrip():
    original = {'global_key': 'test',
                'category': {'name': 'foo', 'index': 75,
                             'thing': {'item': 'thing', 'value': 36.3}}}
    parsed = toml.loads(toml.dumps(original), _dict=UserDict)
    assert isinstance(parsed['category'], UserDict)
    assert toml.loads(toml.dumps(parsed)) == original


def test_mixed_mapping_array():
    value = {'items': [UserDict({'name': 'one',
                                'nested': UserDict({'value': 1})}),
                       UserDict({'name': 'two'})]}
    assert toml.loads(toml.dumps(value)) == value


def test_inline_mapping():
    encoded = toml.TomlEncoder().dump_inline_table(
        UserDict({'value': 1}))
    assert toml.loads('table = ' + encoded) == {'table': {'value': 1}}
