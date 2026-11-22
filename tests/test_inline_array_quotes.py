import pytest

import toml


@pytest.mark.parametrize('value,expected', [
    ('"banan\'as"', "banan'as"),
    ("'a\"b'", 'a"b'),
    ('"a\\\"b"', 'a"b'),
    ("'a\\'", 'a\\'),
    ('"a}b{c,d"', 'a}b{c,d'),
    ('"a\\\\"', 'a\\'),
])
def test_opposite_quotes_and_braces_in_array_of_inline_tables(value, expected):
    document = ('items = [{fruit = "apple"}, {fruit = ' + value +
                '}, {fruit = "cherry"}]')
    assert toml.loads(document) == {
        'items': [{'fruit': 'apple'}, {'fruit': expected}, {'fruit': 'cherry'}]}


def test_nested_tables_with_opposite_quotes():
    document = 'items = [{nested = {value = "it\'s here"}}, {value = "last"}]'
    assert toml.loads(document) == {
        'items': [{'nested': {'value': "it's here"}}, {'value': 'last'}]}
