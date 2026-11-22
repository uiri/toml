import math

import pytest

import toml


@pytest.mark.parametrize('source', [
    'show = all',
    'quality = best',
    'value = hello_world',
    'value = [all]',
    'value = {mode = best}',
])
def test_unquoted_string_error_explains_quotes(source):
    with pytest.raises(toml.TomlDecodeError,
                       match='String values must be quoted') as error:
        toml.loads(source)
    assert error.value.lineno == 1
    assert error.value.colno == 1


def test_quoted_values_and_numeric_specials_are_unchanged():
    parsed = toml.loads('''
show = "all"
quality = 'best'
enabled = true
disabled = false
count = 123
fraction = 1e3
hexadecimal = 0xff
infinity = inf
negative_infinity = -inf
not_a_number = nan
''')
    assert parsed['show'] == 'all'
    assert parsed['quality'] == 'best'
    assert parsed['enabled'] is True
    assert parsed['disabled'] is False
    assert parsed['count'] == 123
    assert parsed['fraction'] == 1000
    assert parsed['hexadecimal'] == 255
    assert math.isinf(parsed['infinity'])
    assert parsed['negative_infinity'] < 0
    assert math.isnan(parsed['not_a_number'])


@pytest.mark.parametrize('source, message', [
    ('value = True', 'Only all lowercase booleans allowed'),
    ('value = 1.', 'This float is missing digits'),
    ('value = 01', 'Weirdness with leading zeroes'),
])
def test_existing_specific_errors_are_preserved(source, message):
    with pytest.raises(toml.TomlDecodeError, match=message):
        toml.loads(source)
