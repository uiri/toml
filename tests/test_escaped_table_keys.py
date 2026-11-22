import pytest

import toml


@pytest.mark.parametrize('header, key', [
    (r'"a\\"', 'a\\'),
    (r'"a\tb"', 'a\tb'),
    (r'"\u0061"', 'a'),
    (r"'a\\'", 'a\\\\'),
])
def test_escaped_table_key(header, key):
    for prefix, suffix, expected in [
        ('[', ']', {key: {'value': 1}}),
        ('[[', ']]', {key: [{'value': 1}]}),
    ]:
        document = prefix + header + suffix + '\nvalue = 1\n'
        assert toml.loads(document) == expected
        assert pytest.importorskip('tomllib').loads(document) == expected
