from __future__ import unicode_literals

import pytest

import toml


@pytest.mark.parametrize('delimiter', ["'''", '"""'])
@pytest.mark.parametrize('body', [
    "hello\n[#if test]\n[/#if]\nabc = '#prop#'\n",
    'one "two #three" four\n',
    'Type="https://example.org/token#PasswordText">\npassword\n',
    "a = '#first#' and b = '#second#'\n",
    "# line entirely inside the string\n",
])
def test_hashes_inside_multiline_strings_are_not_comments(delimiter, body):
    source = ('value = ' + delimiter + '\n' + body + delimiter + '\n'
              '# a real comment after the string\nnext = 1 # another comment')
    assert toml.loads(source) == {'value': body, 'next': 1}


@pytest.mark.parametrize('delimiter', ["'''", '"""'])
def test_comment_after_closing_delimiter_is_still_removed(delimiter):
    source = ('value = ' + delimiter + '\n' + "one '#two' three\n" +
              delimiter + ' # actual comment\nnext = "#kept"\n')
    assert toml.loads(source) == {
        'value': "one '#two' three\n", 'next': '#kept',
    }
