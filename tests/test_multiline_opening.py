import pytest

import toml


@pytest.mark.parametrize('quote', ["'", '"'])
@pytest.mark.parametrize('newlines', range(5))
@pytest.mark.parametrize('array', [False, True])
def test_only_first_newline_after_multiline_delimiter_is_trimmed(
        quote, newlines, array):
    value = quote * 3 + '\n' * newlines + 'first\nsecond' + quote * 3
    expected = '\n' * max(0, newlines - 1) + 'first\nsecond'
    if array:
        value = '[' + value + ']'
        expected = [expected]
    assert toml.loads('value = ' + value) == {'value': expected}


@pytest.mark.parametrize('quote', ["'", '"'])
def test_crlf_immediately_after_multiline_delimiter_is_trimmed(quote):
    source = 'value = ' + quote * 3 + '\r\ntext' + quote * 3
    assert toml.loads(source) == {'value': 'text'}


@pytest.mark.parametrize('quote', ["'", '"'])
def test_newlines_after_multiline_contents_are_preserved(quote):
    source = 'value = ' + quote * 3 + 'first\n\ntext' + quote * 3
    assert toml.loads(source) == {'value': 'first\n\ntext'}


@pytest.mark.parametrize('delimiter', ["'", '"'])
@pytest.mark.parametrize('inner', ["'", '"'])
def test_two_quotes_at_line_end_are_not_an_opening_delimiter(delimiter, inner):
    expected = 'first ' + inner * 2 + '\nsecond ' + inner * 2 + '\n'
    source = 'value = ' + delimiter * 3 + '\n' + expected + delimiter * 3
    assert toml.loads(source) == {'value': expected}


def test_basic_multiline_continuation_still_trims_whitespace():
    source = 'value = """\n\nfirst\\\n  \n  second"""'
    assert toml.loads(source) == {'value': '\nfirstsecond'}
