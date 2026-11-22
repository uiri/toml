import pytest

import toml


@pytest.mark.parametrize('value, expected', [
    ({1: 'a'}, {'1': 'a'}),
    ({1.5: 'a'}, {'1.5': 'a'}),
    ({1: {2: 'a'}}, {'1': {'2': 'a'}}),
    ({'items': [{1: 'a'}]}, {'items': [{'1': 'a'}]}),
])
def test_nonstring_key(value, expected):
    encoded = toml.dumps(value)
    assert toml.loads(encoded) == expected
    assert pytest.importorskip('tomllib').loads(encoded) == expected


@pytest.mark.parametrize('key', [1, 1.5])
def test_inline_nonstring_key(key):
    encoded = 'value = ' + toml.TomlEncoder().dump_inline_table({key: 'a'})
    assert toml.loads(encoded) == {'value': {str(key): 'a'}}
