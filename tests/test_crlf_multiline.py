import io

import pytest

import toml


@pytest.mark.parametrize('quote', ["'''", '"""'])
@pytest.mark.parametrize('trailing_newline', ['', '\r\n', '\n'])
def test_crlf_multiline_keeps_following_keys(quote, trailing_newline):
    document = ('value = ' + quote + 'first\r\nsecond' + quote +
                '\r\nafter = 42' + trailing_newline)
    expected = {'value': 'first\nsecond', 'after': 42}
    assert toml.loads(document) == expected
    assert toml.load(io.StringIO(document)) == expected


def test_crlf_preserves_spaces_in_multiline_content():
    document = 'value = """first\r\n  second  \r\n"""\r\nafter = true\r\n'
    assert toml.loads(document) == {
        'value': 'first\n  second  \n', 'after': True}
