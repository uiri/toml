import pytest

import toml


@pytest.mark.parametrize('value', [
    u'\xa0Non breaking space', u'\x7f', u'\x80', u'\xad',
    u'prefix\x00\x08\x0c\x1f\x7fsuffix',
    u'\\x20', u'\\\\x20', u'\\path\\x20\\',
    u"single ' and double \" quotes", u'\U0001f4a1',
])
def test_string_roundtrip(value):
    # Exercise repeated encoding as well as the independent TOML parser.
    expected = {'value': value}
    current = expected
    for _ in range(3):
        encoded = toml.dumps(current)
        current = toml.loads(encoded)
        assert current == expected
        assert pytest.importorskip('tomllib').loads(encoded) == expected
