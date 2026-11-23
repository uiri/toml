from __future__ import unicode_literals

import pytest

import toml


@pytest.mark.parametrize('source,expected', [
    ('foo = [{bar = "Can\'t parse this"}]',
     {'foo': [{'bar': "Can't parse this"}]}),
    ('foo = [{"isn\'t a bare key" = 42}]',
     {'foo': [{"isn't a bare key": 42}]}),
    ('''foo = [{bar = 'a "quote" and } brace'}]''',
     {'foo': [{'bar': 'a "quote" and } brace'}]}),
    ('foo = [{bar = "isn\'t } a table end"}, {bar = "next"}]',
     {'foo': [{'bar': "isn't } a table end"}, {'bar': 'next'}]}),
    (r'''foo = [{bar = "a \"quote\" isn't a delimiter"}]''',
     {'foo': [{'bar': 'a "quote" isn\'t a delimiter'}]}),
    (r'''foo = [{bar = 'C:\'}, {bar = 'next'}]''',
     {'foo': [{'bar': 'C:\\'}, {'bar': 'next'}]}),
    (r'''foo = [{bar = "C:\\"}, {bar = "next"}]''',
     {'foo': [{'bar': 'C:\\'}, {'bar': 'next'}]}),
    ('foo = [{child = {value = "can\'t"}}, {child = {value = "next"}}]',
     {'foo': [{'child': {'value': "can't"}}, {'child': {'value': 'next'}}]}),
    ('foo = [ {bar = "can\'t"}, {bar = "can"}, ]',
     {'foo': [{'bar': "can't"}, {'bar': 'can'}]}),
])
def test_quotes_inside_inline_tables_do_not_drop_array_elements(
        source, expected):
    assert toml.loads(source) == expected


def test_mixed_quotes_keep_inline_tables_with_custom_dict():
    class CustomDict(dict):
        pass

    parsed = toml.loads('foo = [{bar = "can\'t"}]', _dict=CustomDict)
    assert parsed == {'foo': [{'bar': "can't"}]}
    assert isinstance(parsed['foo'][0], CustomDict)
