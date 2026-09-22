import pytest
import toml


@pytest.mark.parametrize('value, expected', [
    ('"\'"', "'"),
    ('"abc\'def"', "abc'def"),
    ("'a\"b'", 'a"b'),
    ("'path\\'", 'path\\'),
    ('"a\\\"b}"', 'a"b}'),
    ('"{quoted}"', '{quoted}'),
])
def test_quotes_inside_inline_table_arrays(value, expected):
    source = 'foo = [ { x = ' + value + ' }, { y = 2 } ]'
    assert toml.loads(source) == {'foo': [{'x': expected}, {'y': 2}]}


def test_nested_inline_tables_keep_braces_in_strings():
    source = """foo = [{x = {y = "a'b}"}}, {z = '{c"d}'}]"""
    assert toml.loads(source) == {
        'foo': [{'x': {'y': "a'b}"}}, {'z': '{c"d}'}]
    }
