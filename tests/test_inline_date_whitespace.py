import datetime

import pytest

import toml


@pytest.mark.parametrize('space', [' ', '  ', '\t'])
@pytest.mark.parametrize('literal,expected', [
    ('2024-01-01', datetime.date(2024, 1, 1)),
    ('2024-01-01T12:30:00', datetime.datetime(2024, 1, 1, 12, 30)),
])
def test_inline_date_allows_trailing_whitespace(space, literal, expected):
    assert toml.loads('a={b=' + literal + space + '}') == {'a': {'b': expected}}
    assert toml.loads('a={b=' + literal + space + ', c=2}') == {
        'a': {'b': expected, 'c': 2}}


def test_inline_trimming_preserves_quoted_value_whitespace():
    assert toml.loads('a={b=" keep me ", c=2024-01-01 }') == {
        'a': {'b': ' keep me ', 'c': datetime.date(2024, 1, 1)}}
