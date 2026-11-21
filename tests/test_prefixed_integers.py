import pytest

import toml


@pytest.mark.parametrize('separator', ['=', '= ', '=\t'])
@pytest.mark.parametrize('value, expected', [
    ('0xb0', 176),
    ('0xDEAD_BEEF', 3735928559),
    ('0o755', 493),
    ('0o7_5_5', 493),
    ('0b1010', 10),
    ('0b10_10', 10),
])
def test_prefixed_integers_without_whitespace(separator, value, expected):
    assert toml.loads('var' + separator + value) == {'var': expected}


@pytest.mark.parametrize('value, expected', [
    ('0xb0', 176), ('0o755', 493), ('0b1010', 10),
])
def test_prefixed_integer_after_quoted_key_with_equals(value, expected):
    assert toml.loads('"a=b"=' + value + ' # comment') == {'a=b': expected}


@pytest.mark.parametrize('value', [
    '0x', '0xG', '0o8', '0b2', '0x1__2', '0b10_', '+0x1', '-0o1',
])
def test_invalid_prefixed_integers_are_still_rejected(value):
    with pytest.raises(toml.TomlDecodeError):
        toml.loads('var=' + value)
