import pytest

import toml


@pytest.mark.parametrize("value", [
    "first\\\n  second",
    "first\nsecond\\\n  third",
    "first\\\n\n  second",
    "first\\\\\\\n  second",
    "first\\\\\n  second",
    "first\nsecond\\\\\n  third",
])
def test_literal_multiline_backslashes_are_preserved(value):
    assert toml.loads("value = '''" + value + "'''") == {"value": value}


@pytest.mark.parametrize("value", [
    "first\\\n  second",
    "first\nsecond\\\n  third",
    "first\\\\\n  second",
])
def test_literal_multiline_array_backslashes_are_preserved(value):
    document = "value = ['''" + value + "''', '''last''']"
    assert toml.loads(document) == {"value": [value, "last"]}


@pytest.mark.parametrize("first_quote, second_quote, expected", [
    ("'''", '"""', "cd"),
    ('"""', "'''", "c\\\n  d"),
])
def test_multiline_arrays_can_switch_quote_styles(
        first_quote, second_quote, expected):
    document = (
        "value = [" + first_quote + "a\nb" + first_quote + ", " +
        second_quote + "c\\\n  d" + second_quote + "]"
    )
    assert toml.loads(document) == {"value": ["a\nb", expected]}


@pytest.mark.parametrize("value, expected", [
    ("first\\\n  second", "firstsecond"),
    ("first\nsecond\\\n  third", "first\nsecondthird"),
    ("first\\\n\n  second", "firstsecond"),
    ("first\\\\\n  second", "first\\\n  second"),
])
@pytest.mark.parametrize("array", [False, True])
def test_basic_multiline_continuations_still_trim_whitespace(
        value, expected, array):
    literal = '"""' + value + '"""'
    if array:
        assert toml.loads("value = [" + literal + "]") == {"value": [expected]}
    else:
        assert toml.loads("value = " + literal) == {"value": expected}
